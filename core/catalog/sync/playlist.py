# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

from django.utils import timezone

from sync.utils import update_tags, update_image
from sync import api_client

logger = logging.getLogger(__name__)


def get_playlist_media(items):
    for item in items:
        content = item["content"]
        yield {
            # `Media` fields
            "uuid": content.get("uuid"),
            "name": content.get("name").strip(),
            "duration": content.get("duration"),
            # `PlaylistMedia` fields
            "position": item.get("position", 0),
            "cue_in": item.get("cue_in", 0),
            "cue_out": item.get("cue_out", 0),
            "fade_in": item.get("fade_in", 0),
            "fade_out": item.get("fade_out", 0),
            "fade_cross": item.get("fade_cross", 0),
        }


# pylint: disable=too-many-locals
def sync_playlist(playlist):
    # pylint: disable=import-outside-toplevel
    from catalog.models.media import Media

    # pylint: disable=import-outside-toplevel
    from catalog.models.playlist import Series, PlaylistMedia, PlaylistImage

    # pylint: disable=import-outside-toplevel
    from broadcast.models import Editor

    try:
        data = api_client.get(f"playlists/{playlist.uuid}/")
    except api_client.APIClientException as e:
        logger.error(f"unable to get playlist: {playlist} - {e}")
        return None

    update = {
        "name": data.get("name").strip(),
        "updated": timezone.make_aware(datetime.fromisoformat(data.get("updated"))),
    }

    type(playlist).objects.filter(id=playlist.id).update(**update)

    update_tags(playlist, data.get("tags", []))
    update_image(playlist, data.get("image"), PlaylistImage)

    media_list = get_playlist_media(data.get("items", []))

    # TODO: handle safer cleanup of vanished relations
    PlaylistMedia.objects.filter(playlist=playlist).delete()

    for media_dict in media_list:

        uuid = media_dict.pop("uuid")
        name = media_dict.pop("name")
        media_dict.pop("duration")

        try:
            media = Media.objects.get(uuid=uuid)

        except Media.DoesNotExist:
            media = Media(uuid=uuid, name=name, duration=timedelta())
            media.save()

        playlist_media = PlaylistMedia(
            playlist=playlist,
            media=media,
            **media_dict,
        )
        playlist_media.save()

    if data.get("series"):
        series_dict = data.get("series")
        uuid = series_dict.get("uuid")
        name = series_dict.get("name")
        episode = series_dict.get("episode")

        try:
            series = Series.objects.get(uuid=uuid)
            if series.name != name:
                Series.objects.filter(id=series.id).update(name=name)

        except Series.DoesNotExist:
            series = Series(uuid=uuid, name=name)
            series.save()
        series_episode = episode
    else:
        series = None
        series_episode = None

    type(playlist).objects.filter(id=playlist.id).update(
        series=series,
        series_episode=series_episode,
    )

    if data.get("editor"):
        editor_dict = data.get("editor")

        uuid = editor_dict.get("uuid")
        display_name = editor_dict.get("name")

        try:
            editor = Editor.objects.get(uuid=uuid)
            if editor.display_name != display_name:
                Editor.objects.filter(id=editor.id).update(display_name=display_name)

        except Editor.DoesNotExist:
            editor = Editor(uuid=uuid, display_name=display_name)
            editor.save()

        type(playlist).objects.filter(id=playlist.id).update(
            editor=editor,
        )

    logger.info(f"sync completed for {playlist.ct}{playlist.uid}")

    return playlist
