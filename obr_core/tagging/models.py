from django.contrib.contenttypes.models import ContentType
from django.db import models

from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin
from sync.models.mixins import SyncTimeModelMixin

# from taggit.managers import TaggableManager  # NOQA
from taggit.models import GenericTaggedItemBase, TagBase

from .managers import TaggableManager  # NOQA


class TagType(models.TextChoices):
    GENRE = "genre", "Genre"
    MOOD = "mood", "Mood"
    DESCRIPTIVE = "descriptive", "Descriptive"
    INSTRUMENT = "instrument", "Instrument"
    PROFESSION = "profession", "Profession"
    EVENT = "event", "Event"
    LANGUAGE = "language", "Language"


class Tag(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncTimeModelMixin,
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

    @classmethod
    def get_for(cls, queryset):
        ct = ContentType.objects.get_for_model(queryset.model)
        return cls.objects.filter(
            pk__in=TaggedItem.objects.filter(content_type=ct, object_id__in=queryset)
            .values_list("tag", flat=True)
            .distinct(),
        )


class TaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
