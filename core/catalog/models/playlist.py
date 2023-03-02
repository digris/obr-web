from datetime import timedelta

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Max, Q
from django.db.models.functions import Now
from django.utils.functional import cached_property

from base.models.mixins import CTUIDModelMixin, TimestampedModelMixin
from catalog.sync.playlist import sync_playlist
from image.models import BaseSortableImage
from sync.models.mixins import SyncModelMixin
from tagging.models import TaggableManager, TaggedItem


class Playlist(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):
    name = models.CharField(
        max_length=256,
        null=True,
        blank=False,
    )

    series = models.ForeignKey(
        "catalog.Series",
        verbose_name="Series",
        related_name="playlists",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    series_episode = models.PositiveIntegerField(
        verbose_name="Series #",
        null=True,
        blank=True,
    )

    editor = models.ForeignKey(
        to="broadcast.Editor",
        verbose_name="Editor",
        related_name="playlists",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    media = models.ManyToManyField(
        "catalog.Media",
        through="catalog.PlaylistMedia",
        verbose_name="Media",
        related_name="playlists",
        blank=True,
    )

    tags = TaggableManager(
        through=TaggedItem,
        blank=True,
    )

    votes = GenericRelation(
        "rating.Vote",
        related_query_name="playlist",
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"
        ordering = ["-created"]

    def __str__(self):
        if self.series:
            return f"{self.series.name} {self.series_episode or '-'}"
        return str(self.name or self.uid)

    def get_absolute_url(self):
        return f"/discover/playlists/{self.uid}/"

    @cached_property
    def title_display(self):
        title = ""
        if self.series:
            title += f"{self.series.name} "
            if self.series_episode:
                title += f"{self.series_episode} "
            title += "- "
        return f"{title}{self.name}"

    @cached_property
    def image(self):
        return self.images.first()

    @property
    # NOTE: rethink this implementation (currently not in use)
    def airplayed_playlist_media(self):
        qs = self.playlist_media.all()
        qs = qs.annotate(
            latest_airplay=Max(
                "media__airplays__time_start",
                filter=Q(media__airplays__time_start__lte=Now()),
            ),
        )
        qs = qs.filter(latest_airplay__gte=self.emissions.latest().time_start)
        return qs.order_by("position")

    @property
    def latest_emission(self):
        return self.emissions.filter(time_start__lte=Now()).latest()

    @cached_property
    def duration(self):
        total_duration = sum(
            (
                (
                    pm.media.duration
                    - timedelta(milliseconds=pm.cue_in)
                    - timedelta(milliseconds=pm.cue_out)
                )
                for pm in self.playlist_media.all()
            ),
            timedelta(),
        )
        return total_duration

    @cached_property
    def series_dict(self):
        # NOTE: maybe this could be handled in a more elegant way.
        if self.series:
            return {
                "uid": self.series.uid,
                "name": self.series.name,
                "episode": self.series_episode,
            }
        return None

    def sync_data(self, *args, **kwargs):
        return sync_playlist(self, *args, **kwargs)

    def get_emissions(self):
        return list(self.emissions.all()) + list(self.archived_emissions.all())


class Series(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):
    name = models.CharField(
        max_length=256,
        null=True,
        blank=False,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Series"
        verbose_name_plural = "Series"
        ordering = ["name"]

    def __str__(self):
        return str(self.name or self.uid)

    def sync_data(self, *args, **kwargs):
        pass
        # return sync_series(self, *args, **kwargs)

    @property
    def num_playlists(self):
        return self.playlists.count()


class PlaylistMedia(
    CTUIDModelMixin,
    models.Model,
):
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name="playlist_media",
    )
    media = models.ForeignKey(
        "catalog.Media",
        on_delete=models.CASCADE,
        related_name="playlist_media",
    )
    position = models.PositiveIntegerField(
        default=0,
    )
    cue_in = models.PositiveIntegerField(
        default=0,
    )
    cue_out = models.PositiveIntegerField(
        default=0,
    )
    fade_in = models.PositiveIntegerField(
        default=0,
    )
    fade_out = models.PositiveIntegerField(
        default=0,
    )
    fade_cross = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Playlist media"
        verbose_name_plural = "Playlist media"
        db_table = "catalog_playlist_media"
        ordering = ["position"]

    @property
    def effective_duration(self):
        # calculate effective duration, taking into account cues + fade-out
        diff_s = (self.cue_in + self.cue_out + self.fade_cross) / 1000.0
        return self.media.duration - timedelta(seconds=diff_s)


class PlaylistImage(
    BaseSortableImage,
):
    playlist = models.ForeignKey(
        Playlist,
        null=True,
        blank=False,
        related_name="images",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["position"]

    # def __str__(self):
    #     return "{}".format(self.pk)
