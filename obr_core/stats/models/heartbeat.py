from django.db import models
from django.utils import timezone

from common.models.mixins import CTUIDModelMixin


class Heartbeat(
    CTUIDModelMixin,
    models.Model,
):
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    time = models.DateTimeField(
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
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )
    remote_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
    )
    # NOTE: browser & state related. this actually could be derived,
    #       but can be useful to have them here.
    in_foreground = models.BooleanField(
        db_index=True,
    )
    player_source = models.CharField(
        max_length=16,
        db_index=True,
        choices=[
            ("live", "live"),
            ("ondemand", "ondemand"),
            ("unknown", "unknown"),
        ],
    )
    player_state = models.CharField(
        max_length=16,
        db_index=True,
        choices=[
            ("playing", "playing"),
            ("stopped", "stopped"),
            ("paused", "paused"),
            ("buffering", "buffering"),
        ],
    )

    class Meta:
        app_label = "stats"
        verbose_name = "Heartbeat"
        ordering = ["-time"]
        unique_together = ["user_identity", "device_key"]
        db_table = "stats_heartbeat"

    def __str__(self):
        return f"{self.ct}:{self.id}"

    @property
    def time_since_last_heartbeat(self):
        return timezone.now() - self.time
