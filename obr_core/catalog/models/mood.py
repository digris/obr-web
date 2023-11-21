from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.functional import cached_property

from base.models.mixins import CTUIDModelMixin, TimestampedModelMixin
from tagging.models import TaggableManager, TaggedItem


class Mood(TimestampedModelMixin, CTUIDModelMixin, models.Model):
    name = models.CharField(
        max_length=36,
        null=False,
        blank=False,
    )

    teaser = models.CharField(
        max_length=256,
        default="",
        blank=True,
    )

    tags = TaggableManager(
        through=TaggedItem,
        blank=True,
    )

    votes = GenericRelation(
        "rating.Vote",
        related_query_name="mood",
    )

    style = models.JSONField(
        default=dict,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Mood"
        verbose_name_plural = "Moods"
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f"/discover/moods/{self.uid}/"

    @cached_property
    def rgb(self):
        if not self.style:
            return None
        return self.style.get("color")

    @cached_property
    def rays(self):
        if not self.style:
            return []
        return self.style.get("rays", [])
