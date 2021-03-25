from django.db import models
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


class Media(TimestampedModelMixin, CTUIDModelMixin, models.Model):
    class Meta:
        app_label = "catalog"
        verbose_name = "Media"
        verbose_name_plural = "Media"
        ordering = ["-created"]
