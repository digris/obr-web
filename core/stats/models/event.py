from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lead

from base.models.mixins import CTModelMixin, CTUIDModelMixin


class PlayerEventQuerySet(
    models.QuerySet,
):
    def annotate_times_and_durations(self):
        return self.annotate(
            time_end=Window(
                expression=Lead("time"),
                partition_by=[F("user_identity"), F("device_key")],
                order_by=F("time").asc(),
            ),
            duration=F("time_end") - F("time"),
        )


class PlayerEventManager(
    models.Manager,
):
    def get_queryset(self):
        return PlayerEventQuerySet(
            self.model,
            using=self._db,
        ).annotate_times_and_durations()


class PlayerEvent(
    CTModelMixin,
    models.Model,
):
    time = models.DateTimeField(
        db_index=True,
    )
    state = models.CharField(
        max_length=32,
        db_index=True,
    )
    obj_key = models.CharField(
        max_length=32,
        db_index=True,
    )
    source = models.CharField(
        max_length=32,
        db_index=True,
    )
    user_identity = models.CharField(
        max_length=64,
        db_index=True,
    )
    device_key = models.CharField(
        max_length=64,
        db_index=True,
    )
    ingested = models.BooleanField(
        default=False,
        db_index=True,
    )

    objects = PlayerEventManager()

    class Meta:
        app_label = "stats"
        verbose_name = "Player event"
        ordering = ["time"]
        db_table = "stats_player_event"

    def __str__(self):
        return f"{self.ct}:{self.id}"


class StreamEvent(
    CTUIDModelMixin,
    models.Model,
):
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        db_index=True,
    )
    path = models.CharField(
        verbose_name="mountpoint",
        max_length=250,
        blank=True,
        default="",
        db_index=True,
    )
    method = models.CharField(
        verbose_name="request method",
        max_length=6,
        blank=True,
        default="",
        db_index=True,
    )
    status = models.PositiveIntegerField(
        blank=True,
        default="",
        db_index=True,
    )
    bytes_sent = models.PositiveIntegerField(
        default=0,
    )
    referer = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )
    seconds_connected = models.PositiveIntegerField(
        "duration",
        default=0,
        db_index=True,
    )
    time_start = models.DateTimeField(
        db_index=True,
    )
    time_end = models.DateTimeField(
        db_index=True,
    )

    class Meta:
        app_label = "stats"
        verbose_name = "Stream event"
        ordering = ["time_start"]
        db_table = "stats_stream_event"

    def __str__(self):
        return f"{self.ct}:{self.uid}"
