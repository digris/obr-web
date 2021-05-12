# -*- coding: utf-8 -*-
import logging
import re
from datetime import datetime, timedelta

import requests
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone
from google.cloud import storage

logger = logging.getLogger(__name__)


MEDIA_ENDPOINT = "https://www.openbroadcast.org/api/v2/alibrary/media/"


def sync_master_to_gcs(uuid):
    # TODO: change OBP api to uniformly use `media` (instead of `track`)
    master_url = f"{MEDIA_ENDPOINT}{uuid}/download-master/"

    headers = {"Authorization": "Token 0dbea6aeb52acc8f71ed33611b51ded4f0b5bdda"}
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
    fields = [
        "uuid",
        "name",
        "created",
        "updated",
        "artist",
        "release",
        "tracknumber",
        "duration",
        "media_artists",
    ]
    params = {"fields": ",".join(fields)}

    r = requests.get(url=url, params=params)
    data = r.json()

    # print(json.dumps(data, indent=2))

    update = {
        "created": timezone.make_aware(datetime.fromisoformat(data.get("created"))),
        "duration": timedelta(seconds=data.get("duration")),
    }

    type(media).objects.filter(id=media.id).update(**update)

    sync_master_to_gcs(str(media.uuid))

    # related items
    artist_url = data.get("artist")
    # e.g. https://www.openbroadcast.org/api/v2/alibrary/artist/a425f27b-0581-4562-b32d-8bf451b11445/
    if artist_url:
        artist_uuid = artist_url.split("/")[-2]
        logger.debug(f"sync media artist: {artist_uuid}")

        try:
            artist = Artist.objects.get(uuid=artist_uuid)

        except Artist.DoesNotExist:
            artist = Artist(uuid=artist_uuid, name="--init--")
            artist.save()

        MediaArtists.objects.get_or_create(
            media=media,
            artist=artist,
        )

    media_artists = data.get("media_artists", [])
    for media_artist in media_artists:
        artist_uuid = media_artist["uuid"]
        artist_name = media_artist["name"]
        try:
            artist = Artist.objects.get(uuid=artist_uuid)

        except Artist.DoesNotExist:
            artist = Artist(uuid=artist_uuid, name=artist_name)
            artist.save()

        # pylint: disable=unused-variable
        media_artist_obj, created = MediaArtists.objects.get_or_create(
            media=media,
            artist=artist,
        )

        MediaArtists.objects.filter(id=media_artist_obj.id).update(
            position=media_artist["position"],
            join_phrase=media_artist["join_phrase"] or None,
        )

    # related items
    release_url = data.get("release")
    tracknumber = data.get("tracknumber", 0)
    # e.g. https://www.openbroadcast.org/api/v2/alibrary/release/a3c87aae-7a4e-4b27-acf5-4ef2dd5facdf/
    if release_url:
        release_uuid = release_url.split("/")[-2]
        logger.debug(f"sync media release: {release_uuid}")

        try:
            release = Release.objects.get(uuid=release_uuid)

        except Release.DoesNotExist:
            release = Release(uuid=release_uuid, name="--init--")
            release.save()

        release_media, created = ReleaseMedia.objects.get_or_create(
            release=release,
            media=media,
        )

        if tracknumber and tracknumber != release_media.position:
            ReleaseMedia.objects.filter(id=release_media.id).update(
                position=tracknumber,
            )

    logger.info(f"sync completed for media: {media.uid}")

    return media
