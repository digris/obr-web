import itertools
from django.db import transaction
from catalog.models.media import Airplay
from broadcast.models import Emission

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


def foo():
    from broadcast.models import Emission
    import itertools

    flatten = itertools.chain.from_iterable
    qs = Emission.objects.all()
    qs.count()
    all_media = flatten([e.get_media_set() for e in qs])
    all_media = list(flatten([e.get_media_set() for e in qs]))
    all_media
    len(all_media)
    all_media[7]
    from catalog.models.media import Airplay

    aps = []
    for m in all_media:
        aps.append(
            Airplay(time_start=m["time_start"], time_end=m["time_end"], media=media)
        )

    for m in all_media:
        aps.append(Airplay(time_start=m["time_start"], time_end=m["time_end"], media=m))

    for m in all_media:
        aps.append(
            Airplay(
                time_start=m["time_start"], time_end=m["time_end"], media=m["media"]
            )
        )

    len(aps)
    Airplay.objects.bulk_create(aps)
