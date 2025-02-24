import logging
from datetime import datetime

from django.utils import timezone

from sync import api_client
from sync.utils import update_image, update_relations, update_tags

logger = logging.getLogger(__name__)


def sync_label(label, skip_images=False, **kwargs):
    # pylint: disable=import-outside-toplevel
    from catalog.models.label import LabelImage

    try:
        data = api_client.get(f"labels/{label.uuid}/")
    except api_client.APIClientError as e:
        logger.warning(f"unable to get label: {label} - {e}")
        return None

    update = {
        "name": data.get("name").strip(),
        "updated": timezone.make_aware(datetime.fromisoformat(data.get("updated"))),
        "date_start": data.get("date_start"),
        "date_end": data.get("date_end"),
    }

    type(label).objects.filter(id=label.id).update(**update)

    update_relations(label, data.get("relations", []))
    update_tags(label, data.get("tags", []))

    if not skip_images:
        update_image(label, data.get("image"), LabelImage)

    logger.info(f"sync completed for {label.ct}:{label.uid}")

    return label
