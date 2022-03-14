from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin


class IdentifierScope(models.TextChoices):
    MUSICBRAINZ = "musicbrainz", "Musicbrainz"
    OBP = "obp", "open broadcast platform"
    DISCOGS = "discogs", "Discogs"
    WIKIPEDIA = "wikipedia", "Wikipedia"
    OFFICIAL = "official", "Website"
    # NOTE: how to handle scopes that don't make sense for all content-types?
    ISRC = "isrc", "ISRC"


class Identifier(
    TimestampedModelMixin,
    CTUIDModelMixin,
    models.Model,
):

    scope = models.CharField(
        max_length=32,
        choices=IdentifierScope.choices,
        db_index=True,
        null=True,
        blank=False,
    )

    value = models.CharField(
        verbose_name="Identifier",
        max_length=512,
        db_index=True,
        null=True,
        blank=False,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        app_label = "identifier"
        verbose_name = "Identifier"
        verbose_name_plural = "Identifiers"
        unique_together = [
            "scope",
            "value",
            "content_type",
            "object_id",
        ]

    def __str__(self):
        return f"{self.key}"

    @property
    def key(self):
        return f"{self.content_object.ct}:{self.content_object.uid}:{self.scope}"
