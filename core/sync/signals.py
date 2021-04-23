# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.mixins import SyncModelMixin, SyncState

logger = logging.getLogger(__name__)


@receiver(post_save)
# pylint: disable=unused-argument
def sync_model_post_save(sender, instance, **kwargs):
    if not issubclass(sender, SyncModelMixin):
        return

    if instance.sync_state == SyncState.PENDING:
        qs = type(instance).objects.filter(id=instance.id)
        qs.update(sync_state=SyncState.RUNNING)
        logger.debug(f'sync pending for {instance.ct}:{instance.uid} "{instance}"')

        result = instance.sync_data()

        sync_state = SyncState.COMPLETED if result else SyncState.FAILED
        qs.update(sync_state=sync_state)
