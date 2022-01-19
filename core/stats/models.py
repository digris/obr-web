from django.db import models


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

    class Meta:
        app_label = "stats"
        verbose_name = "Player event"
        ordering = ["-time"]
        db_table = "stats_player_event"
        # managed = False
