import logging

from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from catalog.models import Playlist, Media, Airplay
from django.db import transaction
from broadcast.models import Emission
from .settings import ARCHIVE_AFTER_DAYS


logger = logging.getLogger(__name__)


@transaction.atomic
def archive_emissions(database="default"):

    time_end = timezone.now() - timedelta(days=ARCHIVE_AFTER_DAYS)

    logger.info(f"archiving emissions before: {time_end:%Y-%m-%d %H:%M}")

    emission_archive_ids = []
    playlist_qs = Playlist.objects.using(database).all()
    playlist_qs = playlist_qs.prefetch_related(
        "emissions",
    )
    playlist_qs = playlist_qs.annotate(
        num_emissions=Count(
            "emissions",
        ),
    )
    playlist_qs = playlist_qs.filter(num_emissions__gt=1)
    for playlist in playlist_qs:
        ids = (
            playlist.emissions.filter(time_end__lte=time_end)
            .order_by("-time_end")
            .values_list("id", flat=True)[1:]
        )
        if len(ids):
            logger.debug(f"archive {len(ids)} emissions for {playlist}")
        emission_archive_ids += list(ids)

    logger.info(f"archiving {len(emission_archive_ids)} emissions")

    emission_qs = Emission.objects.using(database).filter(id__in=emission_archive_ids)
    for emission in emission_qs:
        emission.delete()

    return len(emission_archive_ids)


@transaction.atomic
def archive_airplays(database="default"):

    time_end = timezone.now() - timedelta(days=ARCHIVE_AFTER_DAYS)

    logger.info(f"archiving airplays before: {time_end:%Y-%m-%d %H:%M}")

    airplay_archive_ids = []
    media_qs = Media.objects.using(database).all()
    media_qs = media_qs.prefetch_related(
        "airplays",
    )
    media_qs = media_qs.annotate(
        num_airplays=Count(
            "airplays",
        ),
    )
    media_qs = media_qs.filter(num_airplays__gt=1)
    for media in media_qs:
        ids = (
            media.airplays.filter(time_end__lte=time_end)
            .order_by("-time_end")
            .values_list("id", flat=True)[1:]
        )
        if len(ids):
            logger.debug(f"archive {len(ids)} airplays for {media}")
        airplay_archive_ids += list(ids)

    logger.info(f"archiving {len(airplay_archive_ids)} airplays")

    airplay_qs = Airplay.objects.using(database).filter(id__in=airplay_archive_ids)
    for airplay in airplay_qs:
        try:
            airplay.delete()
        except transaction.TransactionManagementError as e:
            logger.warning(f"unable to delete {airplay}: {e}")

    return len(airplay_archive_ids)
