from datetime import timedelta
from django.db import models
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


class Media(TimestampedModelMixin, CTUIDModelMixin, models.Model):

    name = models.CharField(max_length=256)

    artists = models.ManyToManyField(
        "catalog.Artist",
        through="catalog.MediaArtists",
        verbose_name="Artists",
        related_name="media",
        blank=True,
    )

    duration = models.DurationField(default=timedelta())

    class Meta:
        app_label = "catalog"
        verbose_name = "Media"
        verbose_name_plural = "Media"
        ordering = ["-created"]

    def __str__(self):
        return self.name

    @property
    def artist_display(self):
        qs = self.media_artist.all()
        return ", ".join(str(ma.artist) for ma in qs)


class MediaArtists(models.Model):

    artist = models.ForeignKey(
        "catalog.Artist",
        on_delete=models.CASCADE,
        related_name="media_artist",
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="media_artist",
    )
    position = models.PositiveSmallIntegerField(
        default=0,
    )
    join_phrase = models.CharField(
        max_length=36,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Media artist"
        verbose_name_plural = "Media artists"
        db_table = "catalog_media_artists"
