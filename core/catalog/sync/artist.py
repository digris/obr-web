# -*- coding: utf-8 -*-
import logging
import json
from datetime import datetime

import requests
from django.utils import timezone
from django.conf import settings
from catalog.sync.utils import update_relations, update_tags, update_image

SYNC_ENDPOINT = getattr(settings, "OBP_SYNC_ENDPOINT")
# SYNC_TOKEN = getattr(settings, "OBP_SYNC_TOKEN")
SYNC_DEBUG = getattr(settings, "OBP_SYNC_DEBUG", False)
ARTIST_ENDPOINT = SYNC_ENDPOINT + "artists/"

logger = logging.getLogger(__name__)


def sync_artist(artist):
    # pylint: disable=import-outside-toplevel
    from catalog.models.artist import ArtistImage

    url = f"{ARTIST_ENDPOINT}{artist.uuid}/"

    r = requests.get(url=url)
    data = r.json()

    if SYNC_DEBUG:
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
        "country_code": data.get("country_code"),
        "date_start": data.get("date_start"),
        "date_end": data.get("date_end"),
    }

    type(artist).objects.filter(id=artist.id).update(**update)

    update_relations(artist, data.get("relations", []))
    update_tags(artist, data.get("tags", []))
    update_image(artist, data.get("image"), ArtistImage)

    logger.info(f"sync completed for {artist.ct}{artist.uid}")

    return artist
