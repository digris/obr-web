from django.conf import settings
from django.db import models

from common.models.mixins import CTUIDModelMixin, TimestampedModelMixin


class SyncProvider(
    models.TextChoices,
):
    SPOTIFY = "spotify", "Spotify"
    DEEZER = "deezer", "Deezer"


class SyncSettings(
    TimestampedModelMixin,
    CTUIDModelMixin,
    models.Model,
):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sync_settings",
        db_index=True,
    )
    provider = models.CharField(
        max_length=16,
        choices=SyncProvider.choices,
        db_index=True,
    )
    remote_uri = models.CharField(
        verbose_name="Remote URI",
        max_length=256,
        blank=True,
        default="",
    )

    class Meta:
        app_label = "streaming_services"
        verbose_name = "Settings"
        verbose_name_plural = "Settings"
        ordering = [
            "-updated",
        ]
        unique_together = [
            "user",
            "provider",
        ]

    def __str__(self):
        return f"{self.user} - {self.provider}"

    @property
    def social_auth(self):
        return self.user.social_auth.filter(provider=self.provider).first()


class RemoteMedia(
    TimestampedModelMixin,
    CTUIDModelMixin,
    models.Model,
):
    name = models.CharField(
        verbose_name="Title",
        max_length=256,
        blank=True,
        default="",
    )
    artist_name = models.CharField(
        verbose_name="Artist",
        max_length=256,
        blank=True,
        default="",
    )
    provider = models.CharField(
        max_length=16,
        choices=SyncProvider.choices,
        db_index=True,
    )
    remote_id = models.CharField(
        verbose_name="Remote ID",
        max_length=256,
        db_index=True,
    )
    remote_uri = models.CharField(
        verbose_name="Remote URI",
        max_length=256,
        db_index=True,
    )
    remote_data = models.JSONField(
        verbose_name="Remote Data",
        default=dict,
    )

    class Meta:
        app_label = "streaming_services"
        verbose_name = "Media (remote)"
        verbose_name_plural = "Media (remote)"
        ordering = [
            "-updated",
        ]
        unique_together = [
            "provider",
            "remote_uri",
        ]

    def __str__(self):
        return f"{self.name} - {self.provider}"
