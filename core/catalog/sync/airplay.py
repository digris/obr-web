import itertools
import logging

from django.db import transaction

from broadcast.models import Emission
from catalog.models.media import Airplay

flatten = itertools.chain.from_iterable

logger = logging.getLogger(__name__)


@transaction.atomic
def sync_airplays(time_start=None):
    airplay_qs = Airplay.objects.all()
    emission_qs = Emission.objects.all()

    if time_start:
        logger.debug(f"sync after {time_start}")
        airplay_qs = airplay_qs.filter(time_start__gte=time_start)
        emission_qs = emission_qs.filter(time_start__gte=time_start)

    logger.info(
        f"sync {emission_qs.count()} emissions - delete {airplay_qs.count()} airplays"
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
            )
        )

    logger.debug(f"creating {len(airplay_objects)} airplay objects")

    Airplay.objects.bulk_create(airplay_objects)
