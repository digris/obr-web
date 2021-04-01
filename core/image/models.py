# -*- coding: utf-8 -*-
import logging
import os
import re

from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from base.models.mixins import CTModelMixin, TimestampedModelMixin, UUIDModelMixin

logger = logging.getLogger(__name__)


def get_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1][1:].strip().lower()
    path = [instance._meta.app_label.lower()]
    path += (
        re.sub("([A-Z])", "_\\1", instance.__class__.__name__)
        .lower()
        .lstrip("_")
        .split("_")
    )
    path += ["{}.{}".format(instance.uuid, ext)]
    return os.path.join(*path)


class BaseImage(
    CTModelMixin,
    TimestampedModelMixin,
    UUIDModelMixin,
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
        return str(self.pk)


class BaseSortableImage(BaseImage):

    position = models.PositiveSmallIntegerField(
        _("Position"), default=1, choices=((x, x) for x in range(1, 100))
    )

    class Meta:
        ordering = ("position",)
        abstract = True

    def __str__(self):
        return str(self.pk)


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
