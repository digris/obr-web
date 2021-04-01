from django.db import models
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


class Artist(TimestampedModelMixin, CTUIDModelMixin, models.Model):

    name = models.CharField(max_length=256)

    class Meta:
        app_label = "catalog"
        verbose_name = "Artist"
        verbose_name_plural = "Artists"
        ordering = ["-created"]

    def __str__(self):
        return self.name
