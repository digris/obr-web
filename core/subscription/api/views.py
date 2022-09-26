import logging

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from subscription.api import serializers
from subscription.utils import plan, voucher

logger = logging.getLogger(__name__)


class SubscriptionPlanView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    @extend_schema(
        responses=serializers.SubscriptionOptionSerializer,
    )
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
    @extend_schema(
        responses=serializers.PaymentOptionSerializer,
    )
    def get(request):
        serializer = serializers.PaymentOptionSerializer(
            {
                "name": "Credit Card",
                "key": "stripe",
                "endpoint": reverse("api:subscription:stripe:endpoint"),
            },
        )
        # data = [
        #     {
        #         "name": "Credit Card",
        #         "key": "stripe",
        #         "endpoint": reverse("api:subscription:stripe:endpoint"),
        #     },
        # ]

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SubscriptionVoucherView(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    throttle_scope = "subscription.voucher"

    @staticmethod
    @extend_schema(
        responses=serializers.VoucherSerializer,
    )
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
    @extend_schema(
        methods={"POST"},
        request=serializers.VoucherSerializer,
        responses=serializers.VoucherSerializer,
    )
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
