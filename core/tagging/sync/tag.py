import logging

from sync import api_client
from tagging.models import TagType

logger = logging.getLogger(__name__)


def sync_tag(tag, delete=False):
    try:
        data = api_client.get(f"tags/{tag.uuid}/")
    except api_client.APIClient404Error:
        logger.info(f"tag does not exist on API: {tag}")
        if delete:
            logger.info(f"delete tag: {tag}")
            tag.delete()
        return None
    except api_client.APIClientError as e:
        logger.error(f"unable to get tag: {tag} - {e}")
        return None

    tag_name = data.get("name")
    tag_type = data.get("type", TagType.GENRE) or TagType.GENRE

    if tag.name == tag_name and tag.type == tag_type:
        logger.debug(f"tag unchanged: {tag}")
        return tag

    tag_qs = type(tag).objects.filter(id=tag.id)
    tag_qs.update(
        name=tag_name,
        type=tag_type,
    )

    logger.info(f"tag updated: {tag} < ({data})")

    return tag
