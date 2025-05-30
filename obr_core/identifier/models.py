from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin


class Identifier(
    TimestampedModelMixin,
    CTUIDModelMixin,
    models.Model,
):
    class Scope(models.TextChoices):
        MUSICBRAINZ = "musicbrainz", "Musicbrainz"
        OBP = "obp", "open broadcast platform"
        DISCOGS = "discogs", "Discogs"
        WIKIPEDIA = "wikipedia", "Wikipedia"
        SOUNDCLOUD = "soundcloud", "SoundCloud"
        OFFICIAL = "official", "Website"
        # NOTE: how to handle scopes that don't make sense for all content-types?
        ISRC = "isrc", "ISRC"
        SPOTIFY = "spotify", "Spotify"
        DEEZER = "deezer", "Deezer"

    class Origin(
        models.TextChoices,
    ):
        OBP = "obp", "OBP"
        CRAWLER = "crawler", "Crawler"

    scope = models.CharField(  # NOQA: DJ001
        verbose_name="Identifier scope",
        max_length=32,
        choices=Scope.choices,
        db_index=True,
        null=True,
        blank=False,
    )
    origin = models.CharField(  # NOQA: DJ001
        max_length=32,
        choices=Origin.choices,
        default=Origin.OBP,
        db_index=True,
    )
    value = models.CharField(  # NOQA: DJ001
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
