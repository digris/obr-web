import re
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

# from django.urls import reverse_lazy
from catalog.models import Playlist

# from broadcast.models import Editor

BASE_META = {
    "fb:app_id": "12345",
    "og:site_name": "open broadcast - radio",
    "og:type": "website",
}

DEFAULT_META = {
    "og:title": _("open broadcast - radio"),
}


def get_playlist_uid(path):
    r = r"^/(discover|collection)/playlists/(?P<uid>[0-9A-F]{8})/$"
    if match := re.search(r, path):
        return match.group("uid")
    return None


def get_playlist_meta(request, uid):
    meta = BASE_META.copy()
    try:
        playlist = Playlist.objects.get(uid=uid)
    except Playlist.DoesNotExist:
        return meta

    language = get_language()
    title = playlist.name
    url = playlist.get_absolute_url()

    meta.update(
        {
            "og:title": title,
            "og:url": request.build_absolute_uri(url),
            "og:locale": f"{language}_CH",
            "og:updated_time": round(playlist.updated.timestamp()),
        }
    )

    if playlist.image:
        image_w = 1200
        image_h = 630
        image_url = f"/images/crop/{image_w}x{image_h}{playlist.image.url}"
        meta.update(
            {
                "og:image": request.build_absolute_uri(image_url),
                "og:image:width": image_w,
                "og:image:height": image_h,
            }
        )

    return meta


def get_default_meta(request):
    meta = (BASE_META | DEFAULT_META).copy()
    language = get_language()
    meta.update(
        {
            "og:url": request.build_absolute_uri(),
            "og:locale": f"{language}_CH",
        }
    )
    return meta


def get_meta_for_request(request):
    if playlist_uid := get_playlist_uid(request.path):
        return get_playlist_meta(request, uid=playlist_uid)

    return get_default_meta(request)
