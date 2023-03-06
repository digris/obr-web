import logging
from datetime import timedelta

from django.db import IntegrityError, transaction
from django.db.models import Count
from django.utils import timezone

from broadcast.models import Emission as BroadcastEmission
from catalog.models import Airplay as CatalogAirplay
from catalog.models import Media, Playlist

from .models import Airplay, Emission
from .settings import ARCHIVE_AFTER_DAYS

logger = logging.getLogger(__name__)


@transaction.atomic
def archive_emissions(database="default"):
    time_end = timezone.now() - timedelta(days=ARCHIVE_AFTER_DAYS)

    logger.info(f"archiving emissions before: {time_end:%Y-%m-%d %H:%M}")

    emission_archive_ids = []
    playlist_qs = Playlist.objects.using(
        alias=database,
    ).all()
    playlist_qs = playlist_qs.prefetch_related(
        "emissions",
    )
    playlist_qs = playlist_qs.annotate(
        num_emissions=Count(
            "emissions",
        ),
    )
    playlist_qs = playlist_qs.filter(
        num_emissions__gt=1,
    )
    for playlist in playlist_qs:
        ids = (
            playlist.emissions.filter(
                time_end__lte=time_end,
            )
            .order_by("-time_end")
            .values_list("id", flat=True)[1:]
        )
        if len(ids):
            logger.debug(f"archive {len(ids)} emissions for {playlist}")
        emission_archive_ids += list(ids)

    logger.info(f"archiving {len(emission_archive_ids)} emissions")

    broadcast_emission_qs = BroadcastEmission.objects.using(
        alias=database,
    ).filter(
        id__in=emission_archive_ids,
    )

    emission_objects = []

    for emission in broadcast_emission_qs:
        emission_objects.append(
            Emission(
                uuid=emission.uuid,
                time_start=emission.time_start,
                time_end=emission.time_end,
                obj_key=emission.obj_key,
                playlist=emission.playlist,
            ),
        )

    Emission.objects.using(
        alias=database,
    ).bulk_create(emission_objects)

    broadcast_emission_qs.delete()

    # emission_qs = Emission.objects.using(
    #     alias=database,
    # ).filter(id__in=emission_archive_ids,)
    # for emission in emission_qs:
    #     emission.delete()

    return len(emission_archive_ids)


@transaction.atomic
def archive_airplays(database="default"):
    time_end = timezone.now() - timedelta(days=ARCHIVE_AFTER_DAYS)

    logger.info(f"archiving airplays before: {time_end:%Y-%m-%d %H:%M}")

    airplay_archive_ids = []
    media_qs = Media.objects.using(
        alias=database,
    ).all()
    media_qs = media_qs.prefetch_related(
        "airplays",
    )
    media_qs = media_qs.annotate(
        num_airplays=Count(
            "airplays",
        ),
    )
    media_qs = media_qs.filter(
        num_airplays__gt=1,
    )
    for media in media_qs:
        ids = (
            media.airplays.filter(
                time_end__lte=time_end,
            )
            .order_by("-time_end")
            .values_list("id", flat=True)[1:]
        )
        if len(ids):
            logger.debug(f"archive {len(ids)} airplays for {media}")
        airplay_archive_ids += list(ids)

    logger.info(f"archiving {len(airplay_archive_ids)} airplays")

    catalog_airplay_qs = CatalogAirplay.objects.using(
        alias=database,
    ).filter(
        id__in=airplay_archive_ids,
    )

    airplay_objects = []

    for airplay in catalog_airplay_qs:
        airplay_objects.append(
            Airplay(
                uuid=airplay.uuid,
                time_start=airplay.time_start,
                time_end=airplay.time_end,
                media=airplay.media,
            ),
        )

    Airplay.objects.using(
        alias=database,
    ).bulk_create(airplay_objects)

    catalog_airplay_qs.delete()

    # bulk_create does not handle `save` (where uid is derived from uuid)
    for e in Emission.objects.filter(
        uid__isnull=True,
    ):
        try:
            Emission.objects.filter(id=e.id).update(
                uid=e.get_uid(),
            )
        except IntegrityError:
            # TODO: check implications.!.
            continue

    # for airplay in airplay_qs:
    #     try:
    #         airplay.delete()
    #     except transaction.TransactionManagementError as e:
    #         logger.warning(f"unable to delete {airplay}: {e}")

    return len(airplay_archive_ids)
