# -*- coding: utf-8 -*-
import logging
import json
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


logger = logging.getLogger(__name__)


PLAYLIST_ENDPOINT = "https://www.openbroadcast.org/api/v2/alibrary/playlist/"


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


def sync_playlist(playlist):
    from catalog.models.media import Media
    from catalog.models.playlist import PlaylistImage, PlaylistMedia

    url = f"{PLAYLIST_ENDPOINT}{playlist.uuid}/"
    fields = [
        "uuid",
        "name",
        "image",
        "created",
        "updated",
        "items",
        "items",
    ]
    params = {"fields": ",".join(fields)}

    r = requests.get(url=url, params=params)
    data = r.json()

    # print(
    #     json.dumps(
    #         {
    #             "url": url,
    #             "data": data,
    #         },
    #         indent=2,
    #     )
    # )

    update = {
        "name": data.get("name").strip(),
        "created": timezone.make_aware(datetime.fromisoformat(data.get("created"))),
    }

    type(playlist).objects.filter(id=playlist.id).update(**update)

    if data.get("image"):
        playlist.images.all().delete()

        image_url = data.get("image")
        # kind uf ugly - we want the 'original' image, not a thumbnail.
        image_url = ".".join(b for b in image_url.split(".")[:-2]).replace(
            "thumbnails/", ""
        )

        ext = image_url.split(".")[-1]
        filename = f"downloaded-image.{ext}"

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()

        i = PlaylistImage(playlist=playlist)
        i.save()
        i.file.save(filename, File(img_temp))

    media_list = get_playlist_media(data.get("items", []))

    # TODO: handle safer cleanup of vanished relations
    PlaylistMedia.objects.filter(playlist=playlist).delete()

    for media_dict in media_list:
        # print(json.dumps(media_dict, indent=2))

        uuid = media_dict.pop("uuid")
        name = media_dict.pop("name")
        media_dict.pop("duration")
        # duration = timedelta(seconds=media_dict.pop("duration"))
        # print("DURATION", duration)

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

    logger.info(f"sync completed for playlist: {playlist.uid}")

    return playlist
