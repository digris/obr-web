from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin
from catalog.sync.artist import sync_artist
from image.models import BaseSortableImage
from sync.models.mixins import SyncModelMixin
from tagging.models import TaggedItem, TaggableManager


class Artist(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):

    name = models.CharField(
        max_length=256,
    )
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

    def sync_data(self, *args, **kwargs):
        return sync_artist(self, *args, **kwargs)


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
        return f"{self.pk}"
