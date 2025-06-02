import logging
from decimal import Decimal

from django.http import HttpResponseRedirect

from common.utils.signer import timestamp_signer
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from subscription.models import Payment, PaymentProvider, PaymentState
from subscription.payment.stripe.checkout import (
    complete_checkout_session,
    create_checkout_session,
    get_checkout_session,
)
from subscription.utils.plan import get_plan_by_sku

logger = logging.getLogger(__name__)


class PaymentCreateSerializer(
    serializers.Serializer,
):
    sku = serializers.CharField(
        required=True,
    )
    donation = serializers.FloatField(
        default=0,
    )
    next = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )


class PaymentSerializer(
    serializers.Serializer,
):
    id = serializers.CharField(
        read_only=True,
    )
    uid = serializers.CharField(
        read_only=True,
    )


class PaymentView(
    APIView,
):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    @extend_schema(
        responses={
            204: None,
        },
        operation_id="stripe_get_payment",
        tags=["subscription-payment"],
    )
    def get(request):
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @staticmethod
    @extend_schema(
        methods=["POST"],
        request=PaymentCreateSerializer,
        responses={
            200: PaymentSerializer,
        },
        operation_id="stripe_create_payment",
        tags=["subscription-payment"],
    )
    def post(request):
        serializer = PaymentCreateSerializer(
            data=request.data,
        )

        user = request.user
        sku = request.data.get("sku")
        donation = request.data.get("donation", 0)
        next_url = request.data.get("next")

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan = get_plan_by_sku(sku)

        if not plan:
            return Response(
                {"sku": ["Invalid SKU"]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items = [
            {
                "sku": plan["sku"],
                "title": plan["title"],
                "price": plan["price"],
            },
        ]

        if donation:
            items.append(
                {
                    "sku": "OBR-D",
                    "title": "Donation",
                    "price": Decimal(abs(donation)),
                },
            )

        total_amount = sum(i["price"] for i in items)
        extra_data = {
            "plan": {
                "sku": plan["sku"],
                "num_days": plan["num_days"],
            },
            "next": next_url,
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
            },
        )


class PaymentSuccessView(
    APIView,
):
    @extend_schema(
        responses={
            301: None,
            302: None,
        },
        operation_id="stripe_payment_success",
        tags=["subscription-payment"],
    )
    def get(self, request, signed_payment_uid):
        payment_uid = timestamp_signer.unsign(signed_payment_uid)
        payment = Payment.objects.get(uid=payment_uid)

        checkout_session = get_checkout_session(request)

        complete_checkout_session(
            session=checkout_session,
            payment=payment,
        )

        if payment.extra_data.get("next"):
            redirect_url = payment.extra_data.get("next")
        else:
            redirect_url = "/account/settings/"

        return HttpResponseRedirect(redirect_url)


class PaymentWebhookView(
    APIView,
):
    @staticmethod
    @extend_schema(
        request=None,
        responses={
            200: None,
        },
        operation_id="stripe_payment_webhook",
        tags=["subscription-payment"],
    )
    # pylint: disable=unused-argument
    def post(request, *args, **kwargs):
        return Response()
