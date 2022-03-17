import logging

from django.conf import settings
from django.db.models.functions import Now
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from broadcast import signals as broadcast_signals
from catalog.sync.airplay import sync_airplays
from .models.mixins import SyncModelMixin, SyncState

SKIP_ALL = getattr(settings, "OBP_SYNC_SKIP_ALL", False)
SKIP_MEDIA = getattr(settings, "OBP_SYNC_SKIP_MEDIA", False)
SKIP_IMAGES = getattr(settings, "OBP_SYNC_SKIP_IMAGES", False)


logger = logging.getLogger(__name__)


@receiver(post_save)
# pylint: disable=unused-argument
def sync_model_post_save(sender, instance, **kwargs):

    if SKIP_ALL:
        return

    if not issubclass(sender, SyncModelMixin):
        return

    if instance.sync_state == SyncState.PENDING:

        qs = type(instance).objects.filter(id=instance.id)
        qs.update(sync_state=SyncState.RUNNING)
        logger.debug(f'sync pending for {instance.ct}:{instance.uid} "{instance}"')

        result = instance.sync_data(
            skip_media=SKIP_MEDIA,
            skip_images=SKIP_IMAGES,
        )

        sync_state = SyncState.COMPLETED if result else SyncState.FAILED
        qs.update(
            sync_state=sync_state,
            sync_last_update=Now(),
        )


@receiver(broadcast_signals.schedule_updated)
# pylint: disable=unused-argument
def schedule_post_update(sender, time_start, time_end, emissions, **kwargs):
    if timezone.is_naive(time_start):
        time_start = timezone.make_aware(time_start)
        logger.debug(f"converted to timezone aware: {time_start}")
    if timezone.is_naive(time_end):
        time_end = timezone.make_aware(time_end)
        logger.debug(f"converted to timezone aware: {time_end}")
    sync_airplays(time_start=time_start, time_end=time_end)
