import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Vote

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Vote)
# pylint: disable=unused-argument
def rating_post_save(sender, instance, created, **kwargs):
    logger.debug(f"rating saved - {instance.value} - {instance.content_object}")
