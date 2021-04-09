# -*- coding: utf-8 -*-0
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.mixins import SyncModelMixin, SyncState


@receiver(post_save)
def sync_model_post_save(sender, instance, **kwargs):
    if not issubclass(sender, SyncModelMixin):
        return

    if instance.sync_state == SyncState.PENDING:
        model = type(instance)
        print("model", model)
        type(instance).objects.filter(id=instance.id).update(
            sync_state=SyncState.RUNNING,
        )

        result = instance.sync_data()
