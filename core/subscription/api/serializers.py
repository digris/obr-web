# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_framework import serializers

from subscription.models import Subscription

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
