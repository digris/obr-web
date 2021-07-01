# -*- coding: utf-8 -*-
import logging
from decimal import Decimal

from django.http import HttpResponseRedirect
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils.signer import timestamp_signer
from subscription.models import Payment, PaymentProvider, PaymentState
from subscription.payment.stripe.checkout import (
    create_checkout_session,
    get_checkout_session,
    complete_checkout_session,
)
from subscription.utils.plan import get_plan_by_sku

logger = logging.getLogger(__name__)


class PaymentSerializer(serializers.Serializer):
    sku = serializers.CharField(required=True)
    donation = serializers.FloatField(default=0)
    next = serializers.CharField(required=False, allow_null=True)


class PaymentView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        return Response()

    def post(self, request):

        serializer = PaymentSerializer(data=request.data)
        user = request.user
        user_uid = str(user.uid)
        sku = request.data.get("sku")
        donation = request.data.get("donation", 0)
        next = request.data.get("next")

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        plan = get_plan_by_sku(sku)

        if not plan:
            return Response(
                {"sku": ["Invalid SKU"]}, status=status.HTTP_400_BAD_REQUEST
            )

        items = [
            {
                "sku": plan["sku"],
                "title": plan["title"],
                "price": plan["price"],
            }
        ]

        if donation:
            items.append(
                {
                    "sku": "OBR-D",
                    "title": "Donation",
                    "price": Decimal(abs(donation)),
                }
            )

        total_amount = sum(i["price"] for i in items)
        extra_data = {
            "plan": {
                "sku": plan["sku"],
                "num_days": plan["num_days"],
            },
            "next": next,
        }

        payment = Payment.objects.create(
            state=PaymentState.PENDING,
            provider=PaymentProvider.STRIPE,
            amount=total_amount,
            user=user,
            extra_data=extra_data,
        )

        checkout_session = create_checkout_session(
            request=request,
            user=user,
            items=items,
            payment=payment,
        )

        payment.state = PaymentState.INITIALIZED
        payment.transaction_id = checkout_session.get("id")
        payment.save()

        return Response(
            {
                "id": checkout_session.id,
                "uid": payment.uid,
            }
        )
        # order = request.data.get("order")
        # order_uuid = order.get("uuid")
        # order = Order.objects.get(uuid=order_uuid)
        # session = create_checkout_session(request=request, order=order)
        # return Response({"id": session.id})


class PaymentSuccessView(APIView):
    def get(self, request, signed_payment_uid):
        payment_uid = timestamp_signer.unsign(signed_payment_uid)
        payment = Payment.objects.get(uid=payment_uid)

        # print("payment_uid", payment_uid)
        # print("payment", payment)

        checkout_session = get_checkout_session(request)

        complete_checkout_session(session=checkout_session, payment=payment)

        redirect_url = payment.extra_data.get("next", "/account/settings/")

        return HttpResponseRedirect(redirect_url)


class PaymentWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        return Response()
        # payload = request.body
        # event = None
        #
        # try:
        #     event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
        # except ValueError as e:
        #     return HttpResponse(status=400)
        #
        # if event.type == "checkout.session.completed":
        #     session = event.data.object
        #     uuid = session.get("client_reference_id")
        #     order = Order.objects.get(uuid=uuid)
        #
        #     complete_checkout_session(session=session, order=order)
        #
        # else:
        #     print("Unhandled event type {}".format(event.type))
        #
        # return HttpResponse(status=200)
