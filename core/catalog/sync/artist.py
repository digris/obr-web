# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from urllib.request import urlopen

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone

logger = logging.getLogger(__name__)


ARTIST_ENDPOINT = "https://www.openbroadcast.org/api/v2/alibrary/artist/"


def sync_artist(artist):
    # pylint: disable=import-outside-toplevel
    from catalog.models.artist import ArtistImage

    url = f"{ARTIST_ENDPOINT}{artist.uuid}/"
    fields = [
        "uuid",
        "name",
        "image",
        "created",
        "updated",
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

    type(artist).objects.filter(id=artist.id).update(**update)

    if data.get("image"):
        artist.images.all().delete()

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

        i = ArtistImage(artist=artist)
        i.save()
        i.file.save(filename, File(img_temp))

    return artist
