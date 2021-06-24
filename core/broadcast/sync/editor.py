# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime

import requests
from django.conf import settings
from django.utils import timezone

from catalog.sync.utils import update_tags, update_image

SYNC_ENDPOINT = getattr(settings, "OBP_SYNC_ENDPOINT")
# SYNC_TOKEN = getattr(settings, "OBP_SYNC_TOKEN")
SYNC_DEBUG = getattr(settings, "OBP_SYNC_DEBUG", False)
EDITOR_ENDPOINT = SYNC_ENDPOINT + "profiles/"

logger = logging.getLogger(__name__)


def sync_editor(editor):
    # pylint: disable=import-outside-toplevel
    from broadcast.models import EditorImage

    url = f"{EDITOR_ENDPOINT}{editor.uuid}/"

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
        "display_name": data.get("name").strip(),
        # "description": data.get("description"),
    }

    type(editor).objects.filter(id=editor.id).update(**update)

    # update_relations(editor, data.get("relations", []))
    update_tags(editor, data.get("tags", []))
    update_image(editor, data.get("image"), EditorImage)

    logger.info(f"sync completed for {editor.ct}{editor.uid}")

    return editor
