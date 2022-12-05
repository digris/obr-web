import logging

from django.db import models

from base.models.mixins import CTUIDModelMixin

logger = logging.getLogger(__name__)


class Airplay(CTUIDModelMixin, models.Model):

    time_start = models.DateTimeField(
        editable=False,
        db_index=True,
        null=False,
        blank=False,
    )

    time_end = models.DateTimeField(
        editable=False,
        db_index=True,
        null=False,
        blank=False,
    )

    media = models.ForeignKey(
        "catalog.Media",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="archived_airplays",
    )

    class Meta:
        app_label = "stats"
        verbose_name = "Airplay (archived)"
        verbose_name_plural = "Airplays (archived)"
        ordering = ["-time_start"]
        get_latest_by = "time_start"

    def __str__(self):
        return f"{self.time_start} - {self.media}"

    @property
    def duration(self):
        return self.time_end - self.time_start
