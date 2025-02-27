from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property

from catalog.sync.label import sync_label
from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin
from image.models import BaseSortableImage
from sync.models.mixins import SyncModelMixin
from tagging.models import TaggableManager, TaggedItem


class Label(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):
    class Kind(models.TextChoices):
        UNDEFINED = "", "-"
        MAJOR = "major", "Major"
        INDEPENDENT = "independent", "Independent"
        NET = "net", "Netlabel"
        EVENT = "event", "Event"

    name = models.CharField(
        max_length=256,
    )
    kind = models.CharField(  # NOQA DJ001
        verbose_name="label type",
        max_length=16,
        blank=True,
        null=True,
        db_index=True,
        choices=Kind.choices,
        default=Kind.UNDEFINED,
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
    root = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
    )
    tags = TaggableManager(
        through=TaggedItem,
        blank=True,
    )
    identifiers = GenericRelation(
        "identifier.Identifier",
        related_name="artist",
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Label"
        verbose_name_plural = "Labels"
        ordering = ["-created"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return None

    @cached_property
    def image(self):
        try:
            return self.images.latest()
        except self.images.model.DoesNotExist:
            return None

    @cached_property
    def num_releases(self):
        return self.releases.count()

    def sync_data(self, *args, **kwargs):
        return sync_label(self, *args, **kwargs)


class LabelImage(BaseSortableImage):
    label = models.ForeignKey(
        Label,
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
