# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin
from broadcast.sync.editor import sync_editor
from image.models import BaseSortableImage
from sync.models.mixins import SyncModelMixin
from tagging.models import TaggedItem, TaggableManager


class EmissionQuerySet(models.QuerySet):
    def upcoming(self):
        now = timezone.now()
        return self.filter(time_start__gt=now)

    def past(self):
        now = timezone.now()
        return self.filter(time_end__lt=now)

    def current(self):
        now = timezone.now()
        return self.filter(time_start__lte=now, time_end__gte=now)


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

    time_end = models.DateTimeField(
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

    objects = EmissionQuerySet.as_manager()

    class Meta:
        app_label = "broadcast"
        verbose_name = "Emission"
        verbose_name_plural = "Emissions"
        ordering = ["-time_start"]
        get_latest_by = "time_start"

    def __str__(self):
        if self.playlist and self.playlist.name:
            return str(self.playlist.name)
        return f"<Emission> {self.uid}"

    @property
    def duration(self):
        if not (self.time_start and self.time_end):
            return None
        return self.time_end - self.time_start

    @property
    def is_current(self):
        now = timezone.now()
        return self.time_start <= now <= self.time_end

    def get_media_set(self):
        if not self.playlist:
            return []

        # print(f"playlist", self.playlist)

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


class Editor(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):

    display_name = models.CharField(
        verbose_name="Display name",
        max_length=256,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        to="account.User",
        verbose_name="User account",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    tags = TaggableManager(
        through=TaggedItem,
        blank=True,
    )

    votes = GenericRelation(
        "rating.Vote",
        related_query_name="editor",
    )

    identifiers = GenericRelation(
        "identifier.Identifier",
        related_name="editor",
    )

    class Meta:
        app_label = "broadcast"
        verbose_name = "Editor"
        verbose_name_plural = "Editors"
        ordering = [
            "display_name",
        ]

    def __str__(self):
        return str(self.display_name or self.uid)

    @cached_property
    def image(self):
        return self.images.first()

    @cached_property
    def num_playlists(self):
        return self.playlists.count()

    def sync_data(self, *args, **kwargs):
        return sync_editor(self, *args, **kwargs)


class EditorImage(BaseSortableImage):

    editor = models.ForeignKey(
        Editor,
        null=True,
        blank=False,
        related_name="images",
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = "broadcast"
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["position"]

    def __str__(self):
        return "{}".format(self.pk)
