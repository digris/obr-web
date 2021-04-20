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


RELEASE_ENDPOINT = "https://www.openbroadcast.org/api/v2/alibrary/release/"


def sync_release(release):
    from catalog.models.media import Media
    from catalog.models.release import ReleaseImage

    url = f"{RELEASE_ENDPOINT}{release.uuid}/"
    fields = [
        "uuid",
        "name",
        "image",
        "created",
        "updated",
        # "releasedate",
        "releasedate_iso",
        # "catalognumber",
        "releasetype",
        # "items",
    ]
    params = {"fields": ",".join(fields)}

    r = requests.get(url=url, params=params)
    data = r.json()

    print(
        json.dumps(
            {
                "url": url,
                "data": data,
            },
            indent=2,
        )
    )

    update = {
        "name": data.get("name").strip(),
        "created": timezone.make_aware(datetime.fromisoformat(data.get("created"))),
        "release_date": data.get("releasedate_iso"),
        "release_type": data.get("releasetype"),
    }

    type(release).objects.filter(id=release.id).update(**update)

    if data.get("image"):
        release.images.all().delete()

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

        i = ReleaseImage(release=release)
        i.save()
        i.file.save(filename, File(img_temp))

    return release
