# -*- coding: utf-8 -*-
import logging

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from subscription.api import serializers
from subscription.utils import trial, plan, voucher

logger = logging.getLogger(__name__)


# class SubscriptionView(APIView):
#     @staticmethod
#     def get(request):
#         user = request.user
#         if user.is_authenticated and hasattr(user, "subscription"):
#             subscription = request.user.subscription
#             serializer = serializers.SubscriptionSerializer(
#                 subscription,
#                 context={
#                     "request": request,
#                 },
#             )
#             response = Response(serializer.data)
#
#         else:
#             response = Response(status=status.HTTP_204_NO_CONTENT)
#
#         return response


class SubscriptionTrialView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    def get(request):
        user = request.user
        if hasattr(user, "subscription"):
            return Response(
                {
                    "message": "Already subscribed. No trial subscription possible.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        options = trial.get_options(user=request.user)
        data = {
            "message": "Get ccess to all content on site without restrictions.",
            "options": options,
        }

        return Response(data)

    @staticmethod
    def put(request):
        user = request.user
        if hasattr(user, "subscription"):
            return Response(
                {
                    "message": "Already subscribed. No trial subscription possible.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        trial.start_trial(user=user)

        data = {
            "location": reverse(
                "api:subscription:subscription",
                request=request,
            ),
        }

        return Response(data, status=status.HTTP_201_CREATED)


class SubscriptionPlanView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    def get(request):
        options = plan.get_options(user=request.user)
        data = {
            "message": "Wähle ein Angebot:",
            "options": options,
        }

        return Response(data)


class PaymentView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    def get(request):
        data = [
            {
                "name": "Credit Card",
                "key": "stripe",
                "endpoint": reverse("api:subscription:stripe:endpoint"),
            },
        ]

        return Response(data)

    # @staticmethod
    # def post(request):
    #     user = request.user
    #     provider = request.data.get("provider")
    #
    #     return Response()


class SubscriptionVoucherView(APIView):

    permission_classes = [
        # permissions.IsAuthenticated,
        permissions.IsAuthenticatedOrReadOnly,
    ]

    throttle_scope = "subscription.voucher"

    @staticmethod
    def get(request):
        code = request.GET.get("code", "")
        code = "".join(code.split("-")).upper()
        try:
            serializer = serializers.VoucherSerializer(
                voucher.get_voucher(
                    user=request.user,
                    code=code,
                ),
                context={
                    "request": request,
                },
            )
            return Response(serializer.data)
        except voucher.VoucherValidationException as e:
            return Response(
                {
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @staticmethod
    def post(request):
        code = request.data.get("code")
        code = "".join(code.split("-")).upper()
        try:
            data = voucher.redeem_voucher(
                user=request.user,
                code=code,
            )
            return Response(data, status.HTTP_201_CREATED)
        except voucher.VoucherValidationException as e:
            return Response(
                {
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
