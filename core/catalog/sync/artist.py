# -*- coding: utf-8 -*-
import logging
import json
from datetime import datetime
from urllib.request import urlopen

import requests
from django.core.files import File
from django.contrib.contenttypes.models import ContentType
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone
from tagging.models import Tag, TaggedItem
from catalog.sync.utils import update_relations, update_tags

logger = logging.getLogger(__name__)


# ARTIST_ENDPOINT = "https://www.openbroadcast.org/api/v2/alibrary/artist/"
ARTIST_ENDPOINT = "https://www.openbroadcast.org/api/v2/obr-sync/artists/"


def sync_artist(artist):
    # pylint: disable=import-outside-toplevel
    from catalog.models.artist import ArtistImage

    print("sa 1", artist.tags.names())

    url = f"{ARTIST_ENDPOINT}{artist.uuid}/"

    r = requests.get(url=url)
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
        "updated": timezone.make_aware(datetime.fromisoformat(data.get("updated"))),
        "name": data.get("name").strip(),
    }

    type(artist).objects.filter(id=artist.id).update(**update)

    artist.tags.set(*[t["name"] for t in data.get("tags", [])], clear=True)

    # for tag in data.get("tags"):
    #     tag_obj, _ = Tag.objects.get_or_create(name=tag["name"])
    #     ct = ContentType.objects.get_for_model(artist)
    #     TaggedItem.objects.get_or_create(
    #         content_type=ct,
    #         object_id=artist.id,
    #         tag=tag_obj,
    #     )
    #     print(tag_obj, TaggedItem)
    #     pass

    update_relations(artist, data.get("relations", []))
    update_tags(artist, data.get("tags", []))

    if data.get("image"):
        artist.images.all().delete()

        image_url = data.get("image")
        ext = image_url.split(".")[-1]
        filename = f"downloaded-image.{ext}"

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()

        i = ArtistImage(artist=artist)
        i.save()
        i.file.save(filename, File(img_temp))

    return artist
