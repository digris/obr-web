import logging

from django.db.models.signals import pre_delete
from django.dispatch import receiver

import donation.models
import donation.services
import stripe
import webhook.signals

logger = logging.getLogger(__name__)


@receiver(webhook.signals.stripe_webhook_received)
# pylint: disable=unused-argument
def on_stripe_webhook_received(sender, event: stripe.Event, **kwargs):

    # NOTE: get events relevant to donations
    #       not very elegant, but good enough for now

    metadata = (
        event.data.object.metadata if hasattr(event.data.object, "metadata") else None
    )

    if not metadata:
        return

    obj_key = metadata.obj_key if hasattr(metadata, "obj_key") else None

    if not obj_key:
        return

    if not obj_key.startswith("donation."):
        return

    donation.services.payment_update_from_event(event=event)


@receiver(pre_delete, sender=donation.models.Donation)
# pylint: disable=unused-argument
def donation_pre_delete(sender, instance, **kwargs):
    try:
        donation.services.donation_cancel_on_stripe(donation=instance)
    except donation.services.ServiceError as e:
        logger.warning(f"Error canceling donation on Stripe: {e}")
