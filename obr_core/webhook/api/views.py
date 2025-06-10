import logging

from django.conf import settings

import stripe
import stripe.error
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from webhook.signals import stripe_webhook_received

logger = logging.getLogger(__name__)


class StripeWebhookView(
    APIView,
):
    # NOTE: shared webhook for incoming stripe events.
    #       events are re-dispatched via signals to be consumed by other apps.

    class InputSerializer(serializers.Serializer):
        # NOTE: at the moment we receive raw payloads from Stripe.
        ...

    class OutputSerializer(serializers.Serializer):
        uid = serializers.CharField()

        class Meta:
            ref_name = "StripeWebhookView"

    @extend_schema(
        operation_id="webhook_stripe",
        responses={status.HTTP_200_OK: OutputSerializer},
        description="Shared stripe webhook endpoint for all events.",
    )
    def post(self, request):

        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                endpoint_secret,
            )
        except ValueError as e:
            logger.error(f"payload validation failed: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"signature verification failed: {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"webhook received: {event.type}")

        stripe_webhook_received.send(
            sender=self,
            event=event,
        )

        return Response(
            {},
            status=status.HTTP_200_OK,
        )
