import logging
import os
import time

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.functional import cached_property

from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin

from .extract import extract_colors, extract_md5

logger = logging.getLogger(__name__)


def get_image_upload_path(instance, filename):
    app = instance.ct.split(".")[0]
    cls = "-".join(instance.ct.split(".")[1:]).replace("image", "")
    ext = os.path.splitext(filename)[1][1:].strip().lower()
    ts = str(hex(int(time.time()))[2:]).upper()
    path = [
        str(app),
        str(cls),
        str(instance.uid),
        f"{ts}.{ext}",
    ]
    return os.path.join(*path)


class BaseImage(
    TimestampedModelMixin,
    CTUIDModelMixin,
    models.Model,
):
    file = models.ImageField(
        "File",
        upload_to=get_image_upload_path,
        null=True,
        blank=False,
    )

    md5_hash = models.CharField(
        max_length=32,
        default="",
    )

    filename = models.CharField(
        verbose_name="Filename",
        max_length=512,
        default="",
        editable=False,
    )

    colors = models.JSONField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk} / {self.uid}"

    @cached_property
    def path(self):
        return str(self.file) if self.file else None

    @cached_property
    def url(self):
        if not self.file:
            return None
        return self.file.url

    @cached_property
    def ratio(self):
        # NOTE: reading width / height results in file access.
        #       value should be extracted on save and stored in db.
        if self.file and self.file.width and self.file.height:
            return round(self.file.width / self.file.height, 5)
        return 1

    @cached_property
    def rgb(self):
        if not self.colors:
            return None
        return self.colors.get("primary")


class BaseSortableImage(BaseImage):
    position = models.PositiveSmallIntegerField(
        "Position",
        default=1,
        choices=((x, x) for x in range(1, 100)),
    )

    class Meta:
        ordering = ("position",)
        abstract = True

    # def __str__(self):


@receiver(pre_save)
# pylint: disable=unused-argument
def image_pre_save(sender, instance=None, **kwargs):
    if not issubclass(sender, BaseImage):
        return

    # pylint: disable=protected-access
    if instance.file and instance.file.name and instance.file._file:  # NOQA: SLF001
        instance.filename = instance.file.name

    if instance.file:
        color, palette = extract_colors(file=instance.file, num_colors=2)
        instance.colors = {
            "primary": color,
            "palette": palette,
        }

    if instance.file:
        instance.md5_hash = extract_md5(file=instance.file)


@receiver(pre_delete)
# pylint: disable=unused-argument
def image_pre_delete(sender, instance, **kwargs):
    if not issubclass(sender, BaseImage):
        return

    try:  # NOQA: SIM105
        instance.file.delete(False)  # NOQA: FBT003
    except Exception:  # NOQA
        pass
