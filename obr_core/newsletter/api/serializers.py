from api_extra.serializers import CTUIDSerializer
from rest_framework import serializers


class NewsletterSerializer(
    CTUIDSerializer,
):
    title = serializers.CharField(
        read_only=True,
    )
    description = serializers.CharField(
        read_only=True,
    )
    is_subscribed = serializers.BooleanField(
        read_only=True,
    )


class SubscriptionSerializer(
    serializers.Serializer,
):
    newsletter_uids = serializers.ListField(
        child=serializers.CharField(),
    )
