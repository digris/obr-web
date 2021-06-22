# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
from urllib.request import urlopen

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone
from django.conf import settings
from catalog.sync.utils import update_relations, update_tags, update_image

SYNC_ENDPOINT = getattr(settings, "OBP_SYNC_ENDPOINT")
# SYNC_TOKEN = getattr(settings, "OBP_SYNC_TOKEN")
SYNC_DEBUG = getattr(settings, "OBP_SYNC_DEBUG", False)
RELEASE_ENDPOINT = SYNC_ENDPOINT + "releases/"

logger = logging.getLogger(__name__)


def sync_release(release):
    # pylint: disable=import-outside-toplevel
    from catalog.models.release import ReleaseImage

    url = f"{RELEASE_ENDPOINT}{release.uuid}/"

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
        "name": data.get("name").strip(),
        "updated": timezone.make_aware(datetime.fromisoformat(data.get("updated"))),
        "release_date": data.get("releasedate"),
        "release_type": data.get("type"),
    }

    type(release).objects.filter(id=release.id).update(**update)

    update_relations(release, data.get("relations", []))
    update_tags(release, data.get("tags", []))
    update_image(release, data.get("image"), ReleaseImage)

    logger.info(f"sync completed for {release.ct}{release.uid}")

    return release
