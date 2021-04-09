from django.db import models
from django.utils.functional import cached_property
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin
from image.models import BaseSortableImage


class Artist(TimestampedModelMixin, CTUIDModelMixin, models.Model):

    name = models.CharField(max_length=256)

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
