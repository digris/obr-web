from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.models.mixins import TimestampedModelMixin


class VoteValue(models.IntegerChoices):
    DOWN = -1, "-"
    UP = 1, "+"


class VoteScope(models.TextChoices):
    UNDEFINED = None, "not specified"
    TRACK = "track", "track"
    EMISSION = "emission", "emission"
    DAYTIME = "daytime", "daytime"
    REPETITION = "repetition", "repetition"


class Vote(TimestampedModelMixin, models.Model):

    value = models.SmallIntegerField(
        blank=False,
        choices=VoteValue.choices,
        db_index=True,
    )

    scope = models.CharField(
        max_length=16,
        null=True,
        choices=VoteScope.choices,
        default=VoteScope.UNDEFINED,
        db_index=True,
    )

    comment = models.TextField(
        max_length=256,
        blank=True,
        default="",
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
        return f"{self.key}"

    @property
    def key(self):
        return f"{self.content_object.ct}:{self.content_object.uid}"
