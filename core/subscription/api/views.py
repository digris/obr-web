import logging

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from subscription.api import serializers
from subscription.models import Voucher
from subscription.utils import plan, voucher

logger = logging.getLogger(__name__)


class PlanView(
    APIView,
):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    @extend_schema(
        responses=serializers.SubscriptionOptionSerializer,
        operation_id="plan_options",
        description="Get available plan options.",
    )
    def get(request):
        options = plan.get_options(user=request.user)
        data = {
            "message": "Wähle ein Angebot:",
            "options": options,
        }

        return Response(data)


class PaymentView(
    APIView,
):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    @staticmethod
    @extend_schema(
        responses=serializers.PaymentOptionSerializer,
        operation_id="payment_options",
        description="Get available payment options.",
    )
    def get(request):
        serializer = serializers.PaymentOptionSerializer(
            {
                "name": "Credit Card",
                "key": "stripe",
                "endpoint": reverse("api:subscription:stripe:endpoint"),
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class VoucherView(
    APIView,
):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    throttle_scope = "subscription.voucher"

    @staticmethod
    @extend_schema(
        responses=serializers.VoucherSerializer,
        operation_id="check_voucher",
        description="Check validity of a voucher for the current user.",
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
        operation_id="redeem_voucher",
        description="Redeem a voucher for the current user.",
    )
    def post(request):
        code = request.data.get("code")
        code = "".join(code.split("-")).upper()
        try:
            data = voucher.redeem_voucher(
                user=request.user,
                code=code,
            )
            return Response(
                data,
                status.HTTP_201_CREATED,
            )
        except voucher.VoucherValidationException as e:
            return Response(
                {
                    "message": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserVoucherView(
    APIView,
):
    @staticmethod
    @extend_schema(
        responses={
            200: serializers.UserVoucherSerializer(many=True),
            204: None,
        },
        operation_id="user_vouchers",
        description="Vouchers that user can provide to other people.",
    )
    def get(request):
        if not request.user.is_authenticated:
            return Response(
                None,
                status.HTTP_204_NO_CONTENT,
            )

        vouchers = Voucher.objects.filter(user=request.user).order_by("-valid_until")
        serializer = serializers.UserVoucherSerializer(vouchers, many=True)
        return Response(
            serializer.data,
            status.HTTP_200_OK,
        )
