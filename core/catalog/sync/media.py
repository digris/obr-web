# -*- coding: utf-8 -*-
import logging
import re
from datetime import datetime, timedelta

from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone
from google.cloud import storage

from sync import api_client
from sync.utils import update_relations, update_tags

logger = logging.getLogger(__name__)


class MasterDownloadException(Exception):
    pass


# def sync_master_to_gcs(media_uuid):
#     try:
#         r = api_client.get(f"media/{media_uuid}/download-master/", raw=True)
#     except api_client.APIClientException as e:
#         raise MasterDownloadException(f"unable to download master: {media_uuid} - {e}")
#
#     filename = re.findall('filename="(.+)"', r.headers["content-disposition"])[0]
#     ext = filename.split(".")[-1]
#     path = f"{media_uuid[0:8].upper()}/master.{ext}"
#
#     client = storage.Client()
#     bucket = client.bucket("obr-master")
#     blob = bucket.blob(path)
#
#     if blob.exists():
#         return path
#
#     with NamedTemporaryFile(delete=True, suffix=f".{ext}") as f:
#         f.write(r.content)
#         f.flush()
#
#         # blob.upload_from_file(f, rewind=True)
#         # NOTE: we upload via name instead of file object to 'detect' content type
#         # (else it is set to application/octet-stream)
#         blob.upload_from_filename(f.name)
#
#     return path


# pylint: disable=too-many-locals
def sync_media(media, skip_media, **kwargs):
    # pylint: disable=import-outside-toplevel
    from catalog.models import Artist, MediaArtists, Release, ReleaseMedia, Master

    try:
        data = api_client.get(f"media/{media.uuid}/")
    except api_client.APIClientException as e:
        logger.error(f"unable to get media: {media} - {e}")
        return None

    update = {
        "updated": timezone.make_aware(datetime.fromisoformat(data.get("updated"))),
        "duration": timedelta(seconds=data.get("duration")),
    }

    type(media).objects.filter(id=media.id).update(**update)

    update_relations(media, data.get("relations", []))
    update_tags(media, data.get("tags", []))

    # try:
    #     sync_master_to_gcs(uuid=str(media.uuid))
    # except MasterDownloadException as e:
    #     logger.error(f"unable to download master: {e}")
    #     return None

    try:
        master = Master.objects.get(media=media)
        logger.debug(f"master exists: {master}")
    except Master.DoesNotExist:
        master = Master(media=media)
        master.save()

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

    logger.info(f"sync completed for {media.ct}:{media.uid}")

    return media


def download_master(media_uuid):
    try:
        r = api_client.get(f"media/{media_uuid}/download-master/", raw=True)
    except api_client.APIClientException as e:
        raise MasterDownloadException(f"unable to download master: {media_uuid} - {e}")

    filename = re.findall('filename="(.+)"', r.headers["content-disposition"])[0]

    return r.content, filename


def sync_master(master, force=False, skip_media=False, **kwargs):

    client = storage.Client()
    bucket = client.bucket("obr-master")

    if master.path and not force:
        # NOTE: implement re-sync
        if bucket.blob(master.path).exists():
            return master

    if skip_media:
        logger.info(f"sync skipping master download {master.ct}:{master.uid}")
        return master

    content, filename = download_master(media_uuid=master.uuid)
    encoding = filename.split(".")[-1].lower()
    path = f"{master.uid}/master.{encoding}"
    blob = bucket.blob(path)

    with NamedTemporaryFile(delete=True, suffix=f".{encoding}") as f:
        f.write(content)
        f.flush()

        # blob.upload_from_file(f, rewind=True)
        # NOTE: we upload via name instead of file object to 'detect' content type
        # (else it is set to application/octet-stream)
        blob.upload_from_filename(f.name)

    update = {
        "encoding": encoding,
        "size": blob.size,
        # "content_type": blob._properties.get("contentType", ""),
        # "md5_hash": blob._properties.get("md5Hash", ""),
        "content_type": blob.content_type,
        "md5_hash": blob.md5_hash,
    }

    type(master).objects.filter(id=master.id).update(**update)

    logger.info(f"sync completed for {master.ct}:{master.uid}")

    return master
