# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from django.utils import timezone

from sync import api_client
from sync.utils import update_relations, update_tags, update_image

logger = logging.getLogger(__name__)


def sync_release(release, skip_images=False, **kwargs):
    # pylint: disable=import-outside-toplevel
    from catalog.models.release import ReleaseImage

    try:
        data = api_client.get(f"releases/{release.uuid}/")
    except api_client.APIClientException as e:
        logger.error(f"unable to get release: {release} - {e}")
        return None

    update = {
        "name": data.get("name").strip(),
        "updated": timezone.make_aware(datetime.fromisoformat(data.get("updated"))),
        "release_date": data.get("releasedate"),
        "release_type": data.get("type"),
    }

    type(release).objects.filter(id=release.id).update(**update)

    update_relations(release, data.get("relations", []))
    update_tags(release, data.get("tags", []))

    if not skip_images:
        update_image(release, data.get("image"), ReleaseImage)

    logger.info(f"sync completed for {release.ct}:{release.uid}")

    return release
