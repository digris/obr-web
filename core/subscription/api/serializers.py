import logging

from django.conf import settings

from api_extra.serializers import CTUIDModelSerializer
from rest_framework import serializers
from subscription.models import Subscription, Voucher

SITE_URL = settings.SITE_URL

logger = logging.getLogger(__name__)


class PaymentOptionSerializer(
    serializers.Serializer,
):
    name = serializers.CharField(
        read_only=True,
    )
    key = serializers.CharField(
        read_only=True,
    )
    endpoint = serializers.URLField(
        read_only=True,
    )


class SubscriptionOptionSerializer(
    serializers.Serializer,
):
    message = serializers.CharField(
        read_only=True,
    )
    # options = serializers.ListSerializer(read_only=True,)  # NOTE: add options schema


class SubscriptionSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    active_until = serializers.DateTimeField(
        read_only=True,
    )

    countries = serializers.ListSerializer(
        read_only=True,
        child=serializers.CharField(min_length=2, max_length=2),
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Subscription
        fields = CTUIDModelSerializer.Meta.fields + [
            "active_until",
            "is_active",
            "is_trial",
            "is_blocked",
            "countries",
        ]


class VoucherSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    is_valid = serializers.BooleanField(
        read_only=True,
    )
    is_valid_for_user = serializers.BooleanField(
        default=False,
        read_only=True,
    )
    until_date = serializers.DateField(
        read_only=True,
        allow_null=True,
    )
    code_display = serializers.CharField(
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Voucher
        fields = CTUIDModelSerializer.Meta.fields + [
            "code",
            "code_display",
            "num_days",
            "is_valid",
            "is_valid_for_user",
            "until_date",
            "valid_until",
        ]


class UserVoucherSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    code_display = serializers.CharField(
        read_only=True,
    )
    is_valid = serializers.BooleanField(
        read_only=True,
    )
    valid_until = serializers.DateTimeField(
        read_only=True,
    )
    num_days = serializers.IntegerField(
        read_only=True,
    )
    max_num_use = serializers.IntegerField(
        read_only=True,
    )
    num_used = serializers.IntegerField(
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Voucher
        fields = CTUIDModelSerializer.Meta.fields + [
            "code_display",
            "is_valid",
            "valid_until",
            "num_days",
            "max_num_use",
            "num_used",
        ]
