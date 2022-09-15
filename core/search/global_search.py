from django.db.models import Count, Max, Q
from catalog.models import Media


def get_results(q):
    media_qs = Media.objects.all()
    media_qs = media_qs.prefetch_related(
        "artists",
        "releases",
        "releases__images",
    )
    media_qs = media_qs.filter(
        Q(name__icontains=q)
        | Q(artists__name__icontains=q)
        | Q(releases__name__icontains=q)
    )

    for media in media_qs[:10]:
        yield {
            "ct": media.ct,
            "uid": media.uid,
            "title": media.name,
            "subtitle": media.artist_display,
            "image": media.image,
        }

    return []
