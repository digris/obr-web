# -*- coding: utf-8 -*-
from django.db import models


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

    class Meta:
        abstract = True

    def sync_data(self):
        raise NotImplementedError("sync_data not implemented")
