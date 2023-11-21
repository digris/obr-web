import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from newsletter import mailchimp
from newsletter.models import Subscription

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Subscription)
# pylint: disable=unused-argument
def subscription_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    mailchimp.subscribe(instance)


@receiver(post_delete, sender=Subscription)
# pylint: disable=unused-argument
def subscription_post_delete(sender, instance, **kwargs):
    if not (instance.newsletter and instance.newsletter.mailchimp_tag):
        return

    mailchimp.unsubscribe(instance)
