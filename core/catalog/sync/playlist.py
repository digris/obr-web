import requests
import json
import time
from datetime import datetime, timedelta
from django.utils import timezone
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


PLAYLIST_ENDPOINT = "https://www.openbroadcast.org/api/v2/alibrary/playlist/"


def sync_playlist(playlist):
    url = f"{PLAYLIST_ENDPOINT}{playlist.uuid}/"
    fields = [
        "uuid",
        "name",
        "image",
        "created",
        "updated",
    ]
    params = {"fields": ",".join(fields)}

    print(url, params)

    r = requests.get(url=url, params=params)

    data = r.json()

    print(json.dumps(data, indent=2))

    print('data.get("name")', data.get("name"))
    playlist.name = data.get("name")

    created = timezone.make_aware(datetime.fromisoformat(data.get("created")))
    playlist.created = created

    type(playlist).objects.filter(id=playlist.id).update(
        name=data.get("name"),
        created=created,
    )

    # updated = timezone.make_aware(datetime.fromisoformat(data.get("updated")))
    # playlist.updated = updated

    # playlist.save()

    if data.get("image"):
        playlist.images.all().delete()
        from catalog.models.playlist import PlaylistImage

        image_url = data.get("image")
        image_url = ".".join(b for b in image_url.split(".")[:-2]).replace(
            "thumbnails/", ""
        )

        ext = image_url.split(".")[-1]
        # filename = f"{playlist.uid}.{ext}"
        filename = f"downloaded-image.{ext}"

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()

        i = PlaylistImage(playlist=playlist)
        i.save()
        i.file.save(filename, File(img_temp))
