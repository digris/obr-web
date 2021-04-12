# -*- coding: utf-8 -*-
import logging
import re
import json
import requests
import subprocess
from datetime import datetime, timedelta
from django.utils import timezone
from urllib.request import urlopen
from django.core.files.temp import NamedTemporaryFile
from google.cloud import storage

logger = logging.getLogger(__name__)


MEDIA_ENDPOINT = "https://www.openbroadcast.org/api/v2/alibrary/media/"


def copy_to_gcs(uuid):

    # nas to tmp
    src = f'5.79.64.65:/nas/storage/prod.openbroadcast.org/media/private/{uuid.replace("-", "/")}/'
    dst = f"data/tmp/{uuid[0:8]}"
    cmd = [
        "rsync",
        "-r",
        src,
        dst,
    ]

    # print(" ".join(cmd))
    try:
        out = subprocess.check_output(" ".join(cmd), shell=True).decode("utf-8")
        # print(out)
    except Exception as e:
        print(e)
        print(" ".join(cmd))
        print("--")
        return

    # tmp to gcs
    src = f"data/tmp/{uuid[0:8]}"
    dst = f"gs://obr-master/{uuid[0:8].upper()}"
    cmd = [
        "gsutil",
        "cp",
        "-r",
        src,
        dst,
    ]

    # print(" ".join(cmd))
    out = subprocess.check_output(" ".join(cmd), shell=True).decode("utf-8")
    # print(out)

    pass


def sync_master_to_gcs(uuid):
    # TODO: change OBP api to uniformly use `media` (instead of `track`)
    master_url = (
        f"{MEDIA_ENDPOINT.replace('/media/', '/track/')}{uuid}/download-master/"
    )

    headers = {"Authorization": "Token 0dbea6aeb52acc8f71ed33611b51ded4f0b5bdda"}
    r = requests.get(master_url, headers=headers)

    print("status", r.status_code)

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


def sync_media(media):
    url = f"{MEDIA_ENDPOINT}{media.uuid}/"
    fields = [
        "uuid",
        "name",
        "created",
        "updated",
        "artist",
        "release",
    ]
    params = {"fields": ",".join(fields)}

    r = requests.get(url=url, params=params)
    data = r.json()

    print(json.dumps(data, indent=2))

    update = {
        "created": timezone.make_aware(datetime.fromisoformat(data.get("created"))),
    }

    type(media).objects.filter(id=media.id).update(**update)

    # copy_to_gcs(str(media.uuid))
    sync_master_to_gcs(str(media.uuid))

    # related items
    artist_url = data.get("artist")
    # e.g. https://www.openbroadcast.org/api/v2/alibrary/artist/a425f27b-0581-4562-b32d-8bf451b11445/
    if artist_url:
        from catalog.models import Artist, MediaArtists

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

    logger.info(f"sync completed for media: {media.uid}")

    return media
