import datetime

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property

from catalog.sync.release import sync_release
from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin
from image.models import BaseSortableImage
from sync.models.mixins import SyncModelMixin
from tagging.models import TaggableManager, TaggedItem


class Release(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):
    name = models.CharField(
        max_length=256,
    )

    release_date = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    release_type = models.CharField(
        max_length=32,
        default="",
        blank=True,
    )

    media = models.ManyToManyField(
        "catalog.Media",
        through="catalog.ReleaseMedia",
        verbose_name="Artists",
        related_name="releases",
        blank=True,
    )

    label = models.ForeignKey(
        "catalog.Label",
        on_delete=models.SET_NULL,
        related_name="releases",
        null=True,
        blank=True,
    )

    tags = TaggableManager(
        through=TaggedItem,
        blank=True,
    )

    votes = GenericRelation(
        "rating.Vote",
        related_query_name="release",
    )

    identifiers = GenericRelation(
        "identifier.Identifier",
        related_name="artist",
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Release"
        verbose_name_plural = "Releases"
        ordering = ["-created"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return None

    @property
    def label_display(self):
        return str(self.label.name) if self.label else ""

    @cached_property
    def image(self):
        try:
            return self.images.latest()
        except self.images.model.DoesNotExist:
            return None

    @cached_property
    def num_media(self):
        return self.media.count()

    @cached_property
    def is_new(self):
        new_after = datetime.date.today() - datetime.timedelta(days=90)
        return bool(self.release_date and self.release_date > new_after)

    def sync_data(self, *args, **kwargs):
        return sync_release(self, *args, **kwargs)


class ReleaseMedia(models.Model):
    release = models.ForeignKey(
        Release,
        on_delete=models.CASCADE,
        related_name="release_media",
    )
    media = models.ForeignKey(
        "catalog.Media",
        on_delete=models.CASCADE,
        related_name="release_media",
    )
    position = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Release media"
        verbose_name_plural = "Release media"
        db_table = "catalog_release_media"
        unique_together = [
            "release",
            "media",
        ]
        ordering = [
            "position",
        ]

    def __str__(self):
        return f"{self.release} <> {self.media}"


class ReleaseImage(BaseSortableImage):
    release = models.ForeignKey(
        Release,
        null=True,
        blank=False,
        related_name="images",
        on_delete=models.CASCADE,
    )

    class Meta(BaseSortableImage.Meta):
        app_label = "catalog"
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["position"]

    def __str__(self):
        return f"{self.pk}"
