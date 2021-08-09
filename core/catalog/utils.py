# -*- coding: utf-8 -*-
from django.db.models import Q

from base.utils.qs import next_in_order, prev_in_order


def get_surounding_media(media):
    preceding = []
    succeeding = []
    qs_pm = media.playlist_media.all()
    qs_pm = qs_pm.select_related(
        "playlist",
        "media",
    )
    qs_pm = qs_pm.prefetch_related(
        "playlist__playlist_media__media",
    )
    for playlist_media in qs_pm:
        # print(f"# playlist: {playlist_media.playlist.name}")

        qs = playlist_media.playlist.playlist_media
        # TODO: implement media type
        qs = qs.exclude(
            Q(media__name__icontains="jingle") | Q(media__name__icontains="station")
        )

        pm = qs.get(position=playlist_media.position)
        previous = prev_in_order(pm, qs=qs)
        next_pm = next_in_order(pm, qs=qs)

        if previous and previous.media not in preceding:
            preceding.append(previous.media)

        if next_pm and next_pm.media not in succeeding:
            succeeding.append(next_pm.media)

    return preceding, succeeding


# pylint: disable=pointless-string-statement
"""
from catalog.models import Media
from broadcast.utils import get_current_media
from catalog.utils import get_surounding_media
media = get_current_media()
media = Media.objects.get(name__iexact="slow dance (voilaa remix)")
get_surounding_media(media)


mqs = Media.objects.all()
for media in mqs[0:1000]:
    get_surounding_media(media)
    
for media in mqs[0:1000]:
    preceding, succeeding = get_surounding_media(media)
    print(f'p: {len(preceding)} - s: {len(succeeding)}')
"""
