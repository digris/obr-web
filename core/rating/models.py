# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from base.models.mixins import TimestampedModelMixin


class VoteValue(models.IntegerChoices):
    DOWN = -1, "-"
    UP = 1, "+"


class Vote(TimestampedModelMixin, models.Model):

    value = models.SmallIntegerField(
        blank=False,
        choices=VoteValue.choices,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="rated_items",
    )

    user_identity = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        app_label = "rating"
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        unique_together = [
            "user",
            "user_identity",
            "content_type",
            "object_id",
        ]

    def __str__(self):
        if self.value:
            return "{}".format(self.value)
        return "{}".format(self.pk)

    @property
    def key(self):
        return f"{self.content_object.ct}:{self.content_object.uid}"
