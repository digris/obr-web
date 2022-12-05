import logging
from datetime import timedelta

from django.db import models
from django.utils import timezone

from base.models.mixins import CTUIDModelMixin

logger = logging.getLogger(__name__)


class Emission(CTUIDModelMixin, models.Model):
    # holds a string based reference to the object:
    # <ct>:<uuid>
    # e.g.
    # alibrary.playlist:86a6c3ec-e8a7-4711-89c2-83e96b45e9db
    obj_key = models.CharField(
        max_length=128,
        editable=False,
        db_index=True,
        null=True,
        blank=False,
    )
    time_start = models.DateTimeField(
        db_index=True,
        null=True,
        blank=False,
    )
    time_end = models.DateTimeField(
        db_index=True,
        null=True,
        blank=False,
    )
    playlist = models.ForeignKey(
        "catalog.Playlist",
        null=True,
        blank=False,
        on_delete=models.CASCADE,
        related_name="archived_emissions",
    )

    class Meta:
        app_label = "stats"
        verbose_name = "Emission (archived)"
        verbose_name_plural = "Emissions (archived)"
        ordering = ["-time_start"]
        get_latest_by = "time_start"

    def __str__(self):
        if self.playlist:
            return str(self.playlist)
        return f"<Emission (archived)> {self.uid}"

    @property
    def duration(self):
        if not (self.time_start and self.time_end):
            return None
        return self.time_end - self.time_start

    @property
    def is_current(self):
        now = timezone.now()
        return self.time_start <= now <= self.time_end

    @property
    def name(self):
        return self.playlist.name if self.playlist else None

    @property
    def series(self):
        return self.playlist.series if self.playlist else None

    def get_media_set(self):
        if not self.playlist:
            return []

        media_set = []
        time_base = self.time_start
        time_offset = timedelta()
        qs = (
            self.playlist.playlist_media.order_by(
                "position",
            )
            .select_related(
                "media",
            )
            .prefetch_related(
                "media__artists",
                "media__media_artist",
                "media__media_artist__artist",
                "media__releases",
                "media__releases__images",
            )
        )
        for playlist_media in qs:
            time_start = time_base + time_offset
            time_end = time_start + playlist_media.effective_duration

            media_set.append(
                {
                    "media": playlist_media.media,
                    "uid": playlist_media.uid,
                    "key": f"{self.uid}-{playlist_media.uid}",
                    "cue_in": playlist_media.cue_in,
                    "cue_out": playlist_media.cue_out,
                    "fade_in": playlist_media.fade_in,
                    "fade_out": playlist_media.fade_out,
                    "fade_cross": playlist_media.fade_cross,
                    "time_start": time_start,
                    "time_end": time_end,
                    "emission": self,
                }
            )

            time_offset += playlist_media.effective_duration

        return media_set
