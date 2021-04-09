from django.db import models
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


class Emission(TimestampedModelMixin, CTUIDModelMixin, models.Model):

    # holds a string based reference to the object:
    # <ct>:<uuid>
    # e.g.
    # alibrary.playlist:86a6c3ec-e8a7-4711-89c2-83e96b45e9db
    obj_key = models.CharField(
        max_length=128,
        editable=False,
        null=True,
        blank=False,
    )

    time_start = models.DateTimeField(
        # editable=False,
        db_index=True,
        null=True,
        blank=False,
    )

    playlist = models.ForeignKey(
        "catalog.Playlist",
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name="emissions",
    )

    class Meta:
        app_label = "broadcast"
        verbose_name = "Emission"
        verbose_name_plural = "Emissions"
        ordering = ["-time_start"]
        get_latest_by = "time_start"

    def __str__(self):
        return self.obj_key
