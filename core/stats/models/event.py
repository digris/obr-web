from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lead


class PlayerEventQuerySet(models.QuerySet):
    def annotate_times_and_durations(self):
        return self.annotate(
            time_end=Window(
                expression=Lead("time"),
                partition_by=[F("user_identity"), F("device_key")],
                order_by=F("time").asc(),
            ),
            duration=F("time_end") - F("time"),
        )


class PlayerEventManager(models.Manager):
    def get_queryset(self):
        return PlayerEventQuerySet(
            self.model, using=self._db
        ).annotate_times_and_durations()


class PlayerEvent(models.Model):
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
        # managed = False
