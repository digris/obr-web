import logging
from datetime import datetime

from django.utils import timezone

from sync import api_client
from sync.utils import update_image, update_tags

logger = logging.getLogger(__name__)


def sync_editor(editor, skip_images=False, **kwargs):
    # pylint: disable=import-outside-toplevel
    from broadcast.models import EditorImage

    try:
        data = api_client.get(f"profiles/{editor.uuid}/")
    except api_client.APIClientError as e:
        logger.error(f"unable to get editor: {editor} - {e}")
        return None

    update = {
        "updated": timezone.make_aware(datetime.fromisoformat(data.get("updated"))),
        "display_name": data.get("name").strip(),
        # "description": data.get("description"),
    }

    type(editor).objects.filter(id=editor.id).update(**update)

    # update_relations(editor, data.get("relations", []))
    update_tags(editor, data.get("tags", []))

    if not skip_images:
        update_image(editor, data.get("image"), EditorImage, clear=False)

    logger.info(f"sync completed for {editor.ct}{editor.uid}")

    return editor
