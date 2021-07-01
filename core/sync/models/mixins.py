# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.utils import timezone


class SyncState(models.TextChoices):
    PENDING = "pending", "Pending"
    RUNNING = "running", "Running"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"


class SyncModelMixin(models.Model):

    sync_state = models.CharField(
        max_length=16,
        db_index=True,
        default=SyncState.PENDING,
        choices=SyncState.choices,
    )

    sync_last_update = models.DateTimeField(
        default=timezone.make_aware(datetime.fromtimestamp(0)),
        db_index=True,
    )

    class Meta:
        abstract = True

    def sync_data(self):
        raise NotImplementedError("sync_data not implemented")
