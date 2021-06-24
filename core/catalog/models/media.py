from datetime import timedelta

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.functions import Now
from django.utils import timezone
from django.utils.functional import cached_property

from base.models.mixins import TimestampedModelMixin, CTUIDModelMixin, CTModelMixin
from catalog.sync.media import sync_media, sync_master
from sync.models.mixins import SyncModelMixin

# from rating.mixins import RatingModelMixin
from tagging.models import TaggedItem, TaggableManager


class Media(
    TimestampedModelMixin,
    CTUIDModelMixin,
    SyncModelMixin,
    models.Model,
):

    name = models.CharField(max_length=256)

    duration = models.DurationField(default=timedelta())

    artists = models.ManyToManyField(
        "catalog.Artist",
        through="catalog.MediaArtists",
        verbose_name="Artists",
        related_name="media",
        blank=True,
    )

    tags = TaggableManager(
        through=TaggedItem,
        blank=True,
    )

    votes = GenericRelation("rating.Vote", related_query_name="media")

    identifiers = GenericRelation(
        "identifier.Identifier",
        related_name="artist",
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Media"
        verbose_name_plural = "Media"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def artist_display(self):
        # return "-"
        qs = self.media_artist.all()
        return ", ".join(str(ma.artist) for ma in qs)

    @cached_property
    def num_airplays(self):
        return self.airplays.count()

    @cached_property
    def latest_airplay(self):
        # This data should normally be prefetched to the queryset.
        latest = (
            self.airplays.filter(time_start__lte=Now()).order_by("-time_start").first()
        )
        return latest.time_start if latest else None
        # return timezone.now()

    def sync_data(self):
        return sync_media(self)


class Master(
    TimestampedModelMixin,
    CTModelMixin,
    SyncModelMixin,
    models.Model,
):

    encoding = models.CharField(
        max_length=4,
        null=True,
    )

    media = models.OneToOneField(
        to=Media,
        on_delete=models.PROTECT,
        related_name="master",
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Master"
        verbose_name_plural = "Masters"

    def __str__(self):
        return str(self.media)

    @property
    def uuid(self):
        return self.media.uuid

    @property
    def uid(self):
        return self.media.uid

    @property
    def path(self):
        if not self.encoding:
            return None
        return f"{self.uid}/master.{self.encoding}"

    def sync_data(self):
        return sync_master(self)


class MediaArtists(models.Model):

    artist = models.ForeignKey(
        "catalog.Artist",
        on_delete=models.CASCADE,
        related_name="media_artist",
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name="media_artist",
    )
    position = models.PositiveSmallIntegerField(
        default=0,
    )
    join_phrase = models.CharField(
        max_length=36,
        null=True,
        blank=True,
    )

    class Meta:
        app_label = "catalog"
        verbose_name = "Media artist"
        verbose_name_plural = "Media artists"
        db_table = "catalog_media_artists"
        ordering = ["position"]


class AirplayQuerySet(models.QuerySet):
    def upcoming(self):
        now = timezone.now()
        return self.filter(time_start__gt=now)

    def past(self):
        now = timezone.now()
        return self.filter(time_end__lt=now)

    def current(self):
        now = timezone.now()
        return self.filter(time_start__lte=now, time_end__gte=now)


class Airplay(TimestampedModelMixin, CTUIDModelMixin, models.Model):

    time_start = models.DateTimeField(
        # editable=False,
        db_index=True,
        null=False,
        blank=False,
    )

    time_end = models.DateTimeField(
        # editable=False,
        db_index=True,
        null=False,
        blank=False,
    )

    media = models.ForeignKey(
        Media,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="airplays",
    )

    objects = AirplayQuerySet.as_manager()

    class Meta:
        app_label = "catalog"
        verbose_name = "Airplay"
        verbose_name_plural = "Airplays"
        ordering = ["-time_start"]
        get_latest_by = "time_start"

    def __str__(self):
        return f"{self.time_start} - {self.media}"

    @property
    def duration(self):
        if not (self.time_start and self.time_end):
            return None
        return self.time_end - self.time_start
