import logging

from django.dispatch import receiver

import catalog.signals
import streaming_services.services

logger = logging.getLogger(__name__)


@receiver(catalog.signals.sync_media_completed)
# pylint: disable=unused-argument
def on_sync_media_completed(sender, media, **kwargs):

    streaming_services.services.media_set_remote_identifiers(
        media=media,
    )
