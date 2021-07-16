# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin
from catalog.sync.playlist import sync_playlist
from image.models import BaseSortableImage
from sync.models.mixins import SyncModelMixin
from tagging.models import TaggedItem, TaggableManager


class Playlist(TimestampedModelMixin, CTUIDModelMixin, SyncModelMixin, models.Model):

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

    series_episode = models.PositiveSmallIntegerField(
        verbose_name="Series #",
        null=True,
        blank=True,
    )

    editor = models.ForeignKey(
        to="broadcast.Editor",
        verbose_name="Editor",
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
        return str(self.name or self.uid)

    def get_absolute_url(self):
        return f"/discover/playlists/{self.uid}/"

    @cached_property
    def image(self):
        return self.images.first()

    def sync_data(self):
        return sync_playlist(self)


class Series(TimestampedModelMixin, CTUIDModelMixin, SyncModelMixin, models.Model):

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
        if not self.name:
            return str(self.uid)
        num_playlists = self.playlists.count()
        return f"{self.name} ({num_playlists})"

    def sync_data(self):
        pass
        # return sync_playlist(self)


class PlaylistMedia(CTUIDModelMixin, models.Model):

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

    @property
    def effective_duration(self):
        # calculate effective duration, taking into account cues + fade-out
        diff_s = (self.cue_in + self.cue_out + self.fade_cross) / 1000.0
        return self.media.duration - timedelta(seconds=diff_s)


class PlaylistImage(BaseSortableImage):

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
