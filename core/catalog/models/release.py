from django.db import models
from django.utils.functional import cached_property
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin
from image.models import BaseSortableImage


class Release(TimestampedModelMixin, CTUIDModelMixin, models.Model):

    name = models.CharField(max_length=256)

    media = models.ManyToManyField(
        "catalog.Media",
        through="catalog.ReleaseMedia",
        verbose_name="Artists",
        related_name="releases",
        blank=True,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Release"
        verbose_name_plural = "Releases"
        ordering = ["-created"]

    def __str__(self):
        return self.name

    @cached_property
    def image(self):
        return self.images.first()

    @cached_property
    def num_media(self):
        return self.media.count()


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


class ReleaseImage(BaseSortableImage):

    release = models.ForeignKey(
        Release,
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
