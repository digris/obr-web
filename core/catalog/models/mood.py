# -*- coding: utf-8 -*-
from django.db import models

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


class Mood(TimestampedModelMixin, CTUIDModelMixin, models.Model):

    name = models.CharField(
        max_length=36,
        null=False,
        blank=False,
    )

    teaser = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Mood"
        verbose_name_plural = "Moods"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f"/discover/moods/{self.uid}/"
