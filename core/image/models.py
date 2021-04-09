# -*- coding: utf-8 -*-
import logging
import os
import time

from urllib.parse import urlparse
from django.db import models
from django.utils.functional import cached_property
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin

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
        _("File"),
        upload_to=get_image_upload_path,
        null=True,
        blank=False,
    )

    filename = models.CharField(
        verbose_name=_("Filename"), max_length=512, null=True, editable=False
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk} / {self.uid}"

    @cached_property
    def path(self):
        # filename does not include bucket in cloud storage
        # so we have to get it out of the url. sorry.
        if not self.url:
            return
        return urlparse(self.url).path[1:]

    @cached_property
    def url(self):
        if not self.file:
            return
        return self.file.url


class BaseSortableImage(BaseImage):

    position = models.PositiveSmallIntegerField(
        _("Position"), default=1, choices=((x, x) for x in range(1, 100))
    )

    class Meta:
        ordering = ("position",)
        abstract = True

    # def __str__(self):
    #     return str(self.pk)


@receiver(pre_save)
# pylint: disable=unused-argument
def image_pre_save(sender, instance=None, **kwargs):
    if not issubclass(sender, BaseImage):
        return

    if instance.file and instance.file.name and instance.file._file:
        instance.filename = instance.file.name


@receiver(pre_delete)
# pylint: disable=unused-argument
def image_pre_delete(sender, instance, **kwargs):
    if not issubclass(sender, BaseImage):
        return

    try:
        instance.file.delete(False)
    except Exception:
        pass
