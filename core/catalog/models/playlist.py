# -*- coding: utf-8 -*-
from datetime import timedelta
from django.db import models
from django.utils.functional import cached_property
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin
from image.models import BaseSortableImage
from sync.models.mixins import SyncModelMixin
from catalog.sync.playlist import sync_playlist


class Playlist(TimestampedModelMixin, CTUIDModelMixin, SyncModelMixin, models.Model):

    name = models.CharField(
        max_length=256,
        null=True,
        blank=False,
    )

    media = models.ManyToManyField(
        "catalog.Media",
        through="catalog.PlaylistMedia",
        verbose_name="Media",
        related_name="playlists",
        blank=True,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"
        ordering = ["-created"]

    def __str__(self):
        return str(self.name or self.uid)

    @cached_property
    def image(self):
        return self.images.first()

    # @cached_property
    # def num_media(self):
    #     return self.media.count()
    #
    # @cached_property
    # def num_emissions(self):
    #     return self.emissions.count()

    def sync_data(self):
        return sync_playlist(self)


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
