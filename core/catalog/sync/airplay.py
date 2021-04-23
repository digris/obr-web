import itertools

from django.db import transaction

from broadcast.models import Emission
from catalog.models.media import Airplay

flatten = itertools.chain.from_iterable


@transaction.atomic
def sync_airplays():
    Airplay.objects.all().delete()

    emission_qs = Emission.objects.all()
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
    Airplay.objects.bulk_create(airplay_objects)
