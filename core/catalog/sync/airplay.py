import itertools
import logging
from datetime import datetime

from django.db import transaction
from django.utils import timezone

from broadcast.models import Emission
from catalog.models.media import Airplay

flatten = itertools.chain.from_iterable

logger = logging.getLogger(__name__)


@transaction.atomic
def sync_airplays(time_start=None, time_end=None):
    airplay_qs = Airplay.objects.all()
    emission_qs = Emission.objects.all()

    if time_start:
        logger.debug(f"sync after {time_start}")
        airplay_qs = airplay_qs.filter(time_start__gte=time_start)
        emission_qs = emission_qs.filter(time_start__gte=time_start)

    if time_end:
        logger.debug(f"sync before {time_end}")
        airplay_qs = airplay_qs.filter(time_start__lte=time_end)
        emission_qs = emission_qs.filter(time_start__lte=time_end)

    logger.debug(
        "sync airplays",
        {
            "current_time": str(timezone.now()),
            "current_time_naive": str(datetime.now()),
            "time_start": str(time_start),
            "num_emissions": emission_qs.count(),
            "num_airplays": airplay_qs.count(),
        },
    )

    logger.info(
        f"sync {emission_qs.count()} emissions - delete {airplay_qs.count()} airplays",
    )

    airplay_qs.delete()

    all_media = list(flatten([e.get_media_set() for e in emission_qs]))

    airplay_objects = []

    for media in all_media:
        airplay_objects.append(
            Airplay(
                time_start=media["time_start"],
                time_end=media["time_end"],
                media=media["media"],
            ),
        )

    logger.debug(f"create {len(airplay_objects)} airplays")

    Airplay.objects.bulk_create(airplay_objects)
