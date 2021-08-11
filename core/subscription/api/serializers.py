# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_framework import serializers

from subscription.models import Subscription, Voucher

SITE_URL = getattr(settings, "SITE_URL")

logger = logging.getLogger(__name__)


class SubscriptionSerializer(serializers.ModelSerializer):
    active_until = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "ct",
            "uid",
            "active_until",
            "is_active",
            "is_trial",
        ]


class VoucherSerializer(serializers.ModelSerializer):
    is_valid_for_user = serializers.BooleanField(
        default=False,
        read_only=True,
    )
    until_date = serializers.DateField(
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Voucher
        fields = [
            "ct",
            "uid",
            "code",
            "code_display",
            "num_days",
            "is_valid",
            "is_valid_for_user",
            "until_date",
            "valid_until",
        ]
