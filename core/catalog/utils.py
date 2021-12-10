from django.db.models import Q  # pragma: no cover

from base.utils.qs import next_in_order, prev_in_order  # pragma: no cover


def get_surounding_media(media):  # pragma: no cover
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
