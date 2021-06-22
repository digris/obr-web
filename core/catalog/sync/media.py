# -*- coding: utf-8 -*-
import logging
import json
import re
from datetime import datetime, timedelta

import requests
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone
from django.conf import settings
from google.cloud import storage
from catalog.sync.utils import update_relations, update_tags

logger = logging.getLogger(__name__)

SYNC_ENDPOINT = getattr(settings, "OBP_SYNC_ENDPOINT")
SYNC_TOKEN = getattr(settings, "OBP_SYNC_TOKEN")
SYNC_DEBUG = getattr(settings, "OBP_SYNC_DEBUG", False)
MEDIA_ENDPOINT = SYNC_ENDPOINT + "media/"


def sync_master_to_gcs(uuid):
    # TODO: change OBP api to uniformly use `media` (instead of `track`)
    master_url = f"{MEDIA_ENDPOINT}{uuid}/download-master/"

    headers = {"Authorization": f"Token {SYNC_TOKEN}"}
    r = requests.get(
        master_url,
        headers=headers,
    )

    # print("status", r.status_code)

    if not r.status_code == 200:
        return False
    filename = re.findall('filename="(.+)"', r.headers["content-disposition"])[0]
    ext = filename.split(".")[-1]

    with NamedTemporaryFile(delete=True, suffix=f".{ext}") as f:
        f.write(r.content)
        f.flush()

        client = storage.Client()
        bucket = client.bucket("obr-master")
        blob = bucket.blob(f"{uuid[0:8].upper()}/master.{ext}")

        # blob.upload_from_file(f, rewind=True)
        # NOTE: we upload via name instead of file object to 'detect' content type
        # (else it is just set to application/octet-stream)
        blob.upload_from_filename(f.name)

    return True


# pylint: disable=too-many-locals
def sync_media(media):
    # pylint: disable=import-outside-toplevel
    from catalog.models import Artist, MediaArtists, Release, ReleaseMedia

    url = f"{MEDIA_ENDPOINT}{media.uuid}/"
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
        "duration": timedelta(seconds=data.get("duration")),
    }

    type(media).objects.filter(id=media.id).update(**update)

    update_relations(media, data.get("relations", []))
    update_tags(media, data.get("tags", []))

    sync_master_to_gcs(str(media.uuid))

    for artist in data.get("artists"):
        uuid = artist.get("uuid")
        name = artist.get("name")
        position = artist.get("position")
        join_phrase = artist.get("join_phrase")
        logger.debug(f"sync media artist: {uuid} - {name}")

        try:
            artist = Artist.objects.get(uuid=uuid)

        except Artist.DoesNotExist:
            artist = Artist(uuid=uuid, name=name)
            artist.save()

        # pylint: disable=unused-variable
        media_artist_obj, created = MediaArtists.objects.get_or_create(
            media=media,
            artist=artist,
        )

        MediaArtists.objects.filter(id=media_artist_obj.id).update(
            position=position,
            join_phrase=join_phrase or None,
        )

    if data.get("release"):
        release_dict = data.get("release")
        uuid = release_dict.get("uuid")
        name = release_dict.get("name")
        position = release_dict.get("position")

        logger.debug(f"sync media release: {uuid} - {name}")

        try:
            release = Release.objects.get(uuid=uuid)

        except Release.DoesNotExist:
            release = Release(uuid=uuid, name=name)
            release.save()

        release_media, created = ReleaseMedia.objects.get_or_create(
            release=release,
            media=media,
        )

        if position and position != release_media.position:
            ReleaseMedia.objects.filter(id=release_media.id).update(
                position=position,
            )

    logger.info(f"sync completed for media: {media.uid}")

    return media
