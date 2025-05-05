import html
import re

from django.conf import settings
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from broadcast.models import Editor
from catalog.models import Artist, Media, Playlist

# see:
# https://ogp.me/
# https://developers.facebook.com/docs/opengraph/music/


DEFAULT_META = [
    ["og:title", _("open broadcast - radio")],
    ["og:type", "music.website"],
]


def get_base_meta(request):
    return [
        ["fb:app_id", "746436298732388"],
        ["og:site_name", "open broadcast - radio"],
        [
            "og:logo",
            request.build_absolute_uri(
                static("assets/share/icon-512x512.png"),
            ),
        ],
    ]


def get_scope_and_uid(path):
    r = r"^/discover/(?P<scope>[a-z]+)/(?P<uid>[0-9A-F]{8})/$"
    if match := re.search(r, path):
        return match.group("scope"), match.group("uid")
    return None, None


def get_image_meta(request, image, w=1200, h=630):
    meta = []

    if not image:
        return meta

    image_url = f"/images/crop/{w}x{h}/{image.path}"
    meta = meta + [
        ["og:image", request.build_absolute_uri(image_url)],
        ["og:image:width", w],
        ["og:image:height", h],
    ]

    return meta


def get_playlist_meta(request, uid):
    try:
        obj = (
            Playlist.objects.select_related(
                "editor",
                "series",
            )
            .prefetch_related(
                "media",
            )
            .get(uid=uid)
        )
    except Playlist.DoesNotExist:
        return get_base_meta(request)

    language = get_language()
    title = obj.title_display
    url = obj.get_absolute_url()

    description = mark_safe(  # NOQA: S308
        html.unescape(
            render_to_string(
                "share/description/_playlist.txt",
                {
                    "obj": obj,
                },
            ),
        ),
    ).replace("\n", " - ")

    meta = [
        ["og:title", title],
        ["og:url", request.build_absolute_uri(url)],
        ["og:type", "music.playlist"],
        ["og:locale", f"{language}_CH"],
        ["og:updated_time", round(obj.updated.timestamp())],
        ["description", description],
    ]

    meta += get_image_meta(request, obj.image, 1200, 1200)

    if editor := obj.editor:
        tags = [f"#{t.name}" for t in obj.tags.exclude(type="descriptive")[:8]]
        description = f"{' '.join(tags)} - curated by {editor}"
        meta += [
            ["og:description", description],
            ["music:creator", request.build_absolute_uri(editor.get_absolute_url())],
        ]

    for index, media in enumerate(obj.media.all()):
        meta += [
            ["music:song", request.build_absolute_uri(media.get_absolute_url())],
            ["music:song:track", index + 1],
        ]

        # for artist in media.artists.all():

    return get_base_meta(request) + meta


def get_artist_meta(request, uid):
    try:
        obj = Artist.objects.get(uid=uid)
    except Artist.DoesNotExist:
        return get_base_meta(request)

    title = obj.name
    url = obj.get_absolute_url()

    description = mark_safe(  # NOQA: S308
        html.unescape(
            render_to_string(
                "share/description/_artist.txt",
                {
                    "obj": obj,
                },
            ),
        ),
    ).replace("\n", " - ")

    meta = [
        ["og:title", title],
        ["og:url", request.build_absolute_uri(url)],
        ["og:type", "profile"],
        ["og:updated_time", round(obj.updated.timestamp())],
        ["description", description],
        ["og:description", description],
    ]

    meta += get_image_meta(request, obj.image, 1200, 1200)

    return get_base_meta(request) + meta


def get_media_meta(request, uid):
    try:
        obj = Media.objects.prefetch_related("artists").get(uid=uid)
    except Media.DoesNotExist:
        return get_base_meta(request)

    title = obj.name
    url = obj.get_absolute_url()

    description = mark_safe(  # NOQA: S308
        html.unescape(
            render_to_string(
                "share/description/_media.txt",
                {
                    "obj": obj,
                },
            ),
        ),
    ).replace("\n", " - ")

    meta = [
        ["og:title", title],
        ["og:url", request.build_absolute_uri(url)],
        ["og:type", "music.song"],
        ["og:updated_time", round(obj.updated.timestamp())],
        ["music:duration", obj.duration.seconds],
        ["description", description],
        ["og:description", description],
    ]

    for artist in obj.artists.all():
        meta = meta + [
            ["music:musician", request.build_absolute_uri(artist.get_absolute_url())],
        ]

    meta += get_image_meta(request, obj.image, 1200, 1200)

    return get_base_meta(request) + meta


def get_editor_meta(request, uid):
    try:
        obj = Editor.objects.get(uid=uid)
    except Editor.DoesNotExist:
        return get_base_meta(request)

    title = obj.display_name
    url = obj.get_absolute_url()

    meta = [
        ["og:title", title],
        ["og:url", request.build_absolute_uri(url)],
        ["og:type", "profile"],
        ["og:updated_time", round(obj.updated.timestamp())],
    ]

    if description := obj.description:
        meta += [
            ["og:description", description],
        ]

    meta += get_image_meta(request, obj.image, 1200, 1200)

    return get_base_meta(request) + meta


def get_radio_meta(request):
    language = get_language()
    meta = [
        ["og:url", request.build_absolute_uri()],
        ["og:locale", f"{language}_CH"],
        ["og:title", _("open broadcast - radio")],
        ["og:description", _("eclectic music")],
        ["og:type", "music.radio_station"],
        #
        [
            "og:image",
            "https://storage.googleapis.com/ch-openbroadcast-media/assets/image/logo-white-on-black.png",
        ],
        ["og:image:width", 622],
        ["og:image:height", 622],
        [
            "description",
            _(
                "Discover eclectic and curated music on open broadcast radio – your gateway to diverse sounds and fresh music picks, streaming anytime, anywhere.",
            ),
        ],
    ]
    if stream_url := getattr(settings, "STREAM_ENDPOINTS", {}).get("icecast"):
        meta = meta + [
            ["og:audio", stream_url],
            ["og:audio:type", "audio/vnd.facebook.bridge"],
        ]

    return get_base_meta(request) + meta


def get_default_meta(request):
    language = get_language()
    meta = [
        ["og:url", request.build_absolute_uri()],
        ["og:locale", f"{language}_CH"],
    ]

    return get_base_meta(request) + DEFAULT_META + meta


def get_meta_for_request(request):
    if request.path == "/":
        return get_radio_meta(request)

    scope, uid = get_scope_and_uid(request.path)

    if scope == "playlists" and uid:
        return get_playlist_meta(request, uid=uid)

    if scope == "tracks" and uid:
        return get_media_meta(request, uid=uid)

    if scope == "artists" and uid:
        return get_artist_meta(request, uid=uid)

    if scope == "editors" and uid:
        return get_editor_meta(request, uid=uid)

    # if media_uid := get_media_uid(request.path):
    # if playlist_uid := get_playlist_uid(request.path):

    return get_default_meta(request)
