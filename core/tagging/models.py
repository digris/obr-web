from django.db import models

from taggit.managers import TaggableManager  # NOQA
from taggit.models import TagBase, GenericTaggedItemBase
from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


class TagType(models.TextChoices):
    GENRE = "genre", "Genre"
    MOOD = "mood", "Mood"
    DESCRIPTIVE = "descriptive", "Descriptive"
    INSTRUMENT = "instrument", "Instrument"
    PROFESSION = "profession", "Profession"
    EVENT = "event", "Event"


class Tag(
    TimestampedModelMixin,
    CTUIDModelMixin,
    TagBase,
):

    type = models.CharField(
        max_length=16,
        db_index=True,
        default=TagType.GENRE,
        choices=TagType.choices,
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return f"{ self.name }"


class TaggedItem(GenericTaggedItemBase):

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
