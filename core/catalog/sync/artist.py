import logging
from datetime import datetime

from django.utils import timezone

from sync import api_client
from sync.utils import update_image, update_relations, update_tags

logger = logging.getLogger(__name__)


def sync_artist(artist, skip_images=False, **kwargs):
    # pylint: disable=import-outside-toplevel
    from catalog.models.artist import ArtistImage

    try:
        data = api_client.get(f"artists/{artist.uuid}/")
    except api_client.APIClientException as e:
        logger.warning(f"unable to get artist: {artist} - {e}")
        return None

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

    if not skip_images:
        update_image(artist, data.get("image"), ArtistImage)

    logger.info(f"sync completed for {artist.ct}:{artist.uid}")

    return artist
