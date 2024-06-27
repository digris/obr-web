import logging

from django.db import models
from django.db.models import F, Window
from django.db.models.functions import Lead
from django.db.models.signals import pre_save
from django.dispatch import receiver

from catalog.models import Media
from common.models.mixins import CTModelMixin, CTUIDModelMixin
from django_countries.fields import CountryField
from geoip import lookup
from user_identity.utils import generate_device_key

logger = logging.getLogger(__name__)


class PlayerEventQuerySet(
    models.QuerySet,
):
    def annotate_times_and_durations(self):
        return self.annotate(
            annotated_time_end=Window(
                expression=Lead("time"),
                partition_by=[F("user_identity"), F("device_key")],
                order_by=F("time").asc(),
            ),
            annotated_duration=F("annotated_time_end") - F("time"),
        )


class PlayerEventManager(
    models.Manager,
):
    def get_queryset(self):
        return PlayerEventQuerySet(
            self.model,
            using=self._db,
        )

    def annotated_times_and_durations(self):
        return self.get_queryset().annotate_times_and_durations()


class PlayerEvent(
    CTModelMixin,
    models.Model,
):
    class State(models.TextChoices):
        PLAYING = "playing", "Playing"
        PAUSED = "paused", "Paused"
        STOPPED = "stopped", "Stopped"
        BUFFERING = "buffering", "Buffering"

    time = models.DateTimeField(
        db_index=True,
    )
    # NOTE: time end is calculated on post-processing
    time_end = models.DateTimeField(
        db_index=True,
        null=True,
        blank=True,
    )
    # NOTE: here we store the maximum possible duration (=duration of media)
    max_duration = models.DurationField(
        db_index=True,
        null=True,
        blank=True,
    )
    state = models.CharField(
        max_length=32,
        db_index=True,
        choices=State.choices,
    )
    obj_key = models.CharField(
        max_length=32,
        db_index=True,
    )
    source = models.CharField(
        max_length=32,
        db_index=True,
    )
    user_identity = models.CharField(
        max_length=64,
        db_index=True,
    )
    device_key = models.CharField(
        max_length=64,
        db_index=True,
    )
    ingested = models.BooleanField(
        default=False,
        db_index=True,
    )

    objects = PlayerEventManager()

    class Meta:
        app_label = "stats"
        verbose_name = "Player event"
        ordering = ["time"]
        db_table = "stats_player_event"

    def __str__(self):
        return f"{self.ct}:{self.id}"


@receiver(pre_save, sender=PlayerEvent)
def player_event_pre_save(sender, instance, **kwargs):
    if instance.state == "playing" and not instance.max_duration:
        _, media_uid = instance.obj_key.split(":")
        try:
            media = Media.objects.get(uid=media_uid)
            instance.max_duration = media.duration
            logger.debug(f"max duration set to {media.duration}")
        except Media.DoesNotExist:
            return


class StreamEvent(
    CTUIDModelMixin,
    models.Model,
):
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        db_index=True,
    )
    path = models.CharField(
        verbose_name="mountpoint",
        max_length=250,
        blank=True,
        default="",
        db_index=True,
    )
    method = models.CharField(
        verbose_name="request method",
        max_length=6,
        blank=True,
        default="",
        db_index=True,
    )
    status = models.PositiveIntegerField(
        blank=True,
        default="",
        db_index=True,
    )
    bytes_sent = models.PositiveIntegerField(
        default=0,
    )
    referer = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )
    seconds_connected = models.PositiveIntegerField(
        "duration",
        default=0,
        db_index=True,
    )
    time_start = models.DateTimeField(
        db_index=True,
    )
    time_end = models.DateTimeField(
        db_index=True,
    )
    device_key = models.CharField(
        max_length=64,
        db_index=True,
        default="",
        blank=True,
    )
    geoip_city = models.CharField(
        verbose_name="city",
        max_length=128,
        blank=True,
        default="",
        db_index=True,
    )
    geoip_region = models.CharField(
        verbose_name="region",
        max_length=128,
        blank=True,
        default="",
        db_index=True,
    )
    geoip_country = CountryField(
        verbose_name="country",
        blank=True,
        default="",
        db_index=True,
    )

    class Meta:
        app_label = "stats"
        verbose_name = "Stream event"
        ordering = ["time_start"]
        db_table = "stats_stream_event"

    def __str__(self):
        return f"{self.ct}:{self.uid}"


@receiver(pre_save, sender=StreamEvent)
def stream_event_pre_save(sender, instance, **kwargs):
    if instance.ip:
        instance.device_key = generate_device_key(
            instance.ip,
            instance.user_agent,
        )

    if instance.ip:
        try:
            geoip_data = lookup.geoip(instance.ip)
            instance.geoip_city = geoip_data.get("city", "")[:128]
            instance.geoip_region = geoip_data.get("region", "")[:128]
            instance.geoip_country = geoip_data.get("country_code", "")
        except lookup.GeoipError as e:
            logger.info(f"geoip error: {e}")
