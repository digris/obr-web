# -*- coding: utf-8 -*-
from django.db import models
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import GenericRelation

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin
from sync.models.mixins import SyncModelMixin
from image.models import BaseSortableImage
from tagging.models import TaggedItem, TaggableManager
from catalog.sync.artist import sync_artist


class Artist(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):

    name = models.CharField(max_length=256)

    country_code = models.CharField(
        verbose_name="Country",
        max_length=2,
        null=True,
        blank=True,
        db_index=True,
    )

    date_start = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    date_end = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    tags = TaggableManager(
        through=TaggedItem,
        blank=True,
    )

    votes = GenericRelation(
        "rating.Vote",
        related_query_name="artist",
    )

    identifiers = GenericRelation(
        "identifier.Identifier",
        related_name="artist",
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Artist"
        verbose_name_plural = "Artists"
        ordering = ["-created"]

    def __str__(self):
        return self.name

    @cached_property
    def image(self):
        return self.images.first()

    def sync_data(self):
        return sync_artist(self)


class ArtistImage(BaseSortableImage):

    artist = models.ForeignKey(
        Artist,
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

    def __str__(self):
        return "{}".format(self.pk)
