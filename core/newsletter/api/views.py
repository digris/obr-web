import logging

from django.db.models import Count, Q

from drf_spectacular.utils import extend_schema
from newsletter.models import Newsletter, Subscription
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers

logger = logging.getLogger(__name__)


class NewsletterView(APIView):

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        qs = Newsletter.objects.annotate(
            is_subscribed=Count(
                "subscriptions",
                filter=Q(
                    subscriptions__user=self.request.user,
                ),
            ),
        )
        return qs

    @extend_schema(
        responses={
            200: serializers.NewsletterSerializer(many=True),
        },
        operation_id="newsletters",
    )
    def get(self, request):
        serializer = serializers.NewsletterSerializer(
            self.get_queryset(),
            many=True,
        )
        return Response(serializer.data)

    @extend_schema(
        request=serializers.SubscriptionSerializer,
        responses={
            200: serializers.NewsletterSerializer(many=True),
        },
        operation_id="subscribe",
    )
    def post(self, request):

        serializer = serializers.SubscriptionSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        newsletter_uids = serializer.data.get("newsletter_uids", [])

        for uid in newsletter_uids:
            if newsletter := Newsletter.objects.get(uid=uid):
                Subscription.objects.get_or_create(
                    newsletter=newsletter, user=request.user
                )

        Subscription.objects.exclude(newsletter__uid__in=newsletter_uids).delete()

        response_serializer = serializers.NewsletterSerializer(
            self.get_queryset(),
            many=True,
        )
        return Response(response_serializer.data)
