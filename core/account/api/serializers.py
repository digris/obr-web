# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.urls import reverse_lazy, reverse
from rest_framework import serializers
from rest_flex_fields.serializers import FlexFieldsSerializerMixin

from account.models import User, Settings
from social_django.models import UserSocialAuth

SITE_URL = getattr(settings, "SITE_URL")

logger = logging.getLogger(__name__)


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = [
            "id",
        ]


class UserSerializer(FlexFieldsSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "ct",
            "uid",
            "email",
            "date_joined",
            "signup_completed",
            "first_name",
            "last_name",
            # "full_name",
        ]
        expandable_fields = {
            "settings": SettingsSerializer,
        }


class SocialBackendSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            "provider": instance,
            "connect_url": reverse(
                "social:begin",
                kwargs={
                    "backend": str(instance),
                },
            ),
        }


class ConnectedSocialBackendSerializer(serializers.ModelSerializer):
    can_disconnect = serializers.SerializerMethodField()
    disconnect_url = serializers.SerializerMethodField()

    class Meta:
        model = UserSocialAuth
        fields = [
            "provider",
            "uid",
            "can_disconnect",
            "disconnect_url",
        ]

    def get_can_disconnect(self, obj):
        return obj.allowed_to_disconnect(
            user=obj.user,
            backend_name=str(obj.provider),
            association_id=obj.id,
        )

    def get_disconnect_url(self, obj):
        return reverse(
            "social:disconnect_individual",
            kwargs={
                "backend": str(obj.provider),
                "association_id": obj.id,
            },
            # args=[str(obj.provider)],
        )


class SocialBackendsSerializer(serializers.Serializer):
    connected = ConnectedSocialBackendSerializer(
        many=True,
        read_only=True,
    )
    disconnected = SocialBackendSerializer(
        many=True,
        read_only=True,
    )
    all = SocialBackendSerializer(
        many=True,
        read_only=True,
    )
