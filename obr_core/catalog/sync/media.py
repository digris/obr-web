import hashlib
import logging
import mimetypes
import os
import re
import shutil
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone

from catalog.signals import sync_media_completed
from google.cloud import storage
from identifier.models import Identifier
from sync import api_client
from sync.utils import update_identifier, update_relations, update_tags

logger = logging.getLogger(__name__)


class MasterDownloadError(Exception):
    pass


# pylint: disable=too-many-locals, unused-argument
def sync_media(media, skip_media=False, **kwargs):
    # pylint: disable=import-outside-toplevel
    from catalog.models import Artist, Master, MediaArtists, Release, ReleaseMedia

    if media.sync_excluded:
        return None

    try:
        data = api_client.get(f"media/{media.uuid}/")
    except api_client.APIClientError as e:
        logger.warning(f"unable to get media: {media} - {e}")
        return None

    update = {
        "updated": timezone.make_aware(datetime.fromisoformat(data.get("updated"))),
        "name": data.get("name").strip(),
        "duration": timedelta(seconds=data.get("duration")),
        "kind": data.get("type") or "",
    }

    type(media).objects.filter(id=media.id).update(**update)

    update_relations(media, data.get("relations", []))

    update_tags(media, data.get("tags", []))

    update_identifier(media, Identifier.Scope.ISRC, data.get("isrc"))

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
        join_phrase = artist.get("join_phrase", "")
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
            join_phrase=join_phrase or "",
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

    sync_media_completed.send(
        sender=None,
        media=media,
    )

    logger.info(f"sync completed for {media.ct}:{media.uid}")

    return media


def download_master(media_uuid):
    try:
        r = api_client.get(f"media/{media_uuid}/download-master/", raw=True)
    except api_client.APIClientError as e:
        raise MasterDownloadError(
            f"unable to download master: {media_uuid} - {e}",
        ) from e

    filename = re.findall('filename="(.+)"', r.headers["content-disposition"])[0]

    return r.content, filename


def sync_master(master, force=False, skip_media=False, **kwargs):
    if skip_media:
        logger.info(f"sync skipping master download {master.ct}:{master.uid}")
        return master

    if (
        settings.STORAGES["default"]["BACKEND"]
        == "storages.backends.gcloud.GoogleCloudStorage"
    ):
        mode = "gs"
    else:
        mode = "fs"

    try:
        content, filename = download_master(media_uuid=master.uuid)
    except MasterDownloadError as e:
        logger.error(f"unable to download master: {master} - {e}")
        return None

    encoding = filename.split(".")[-1].lower()
    path = f"{master.uid}/master.{encoding}"

    update = {}

    with NamedTemporaryFile(delete=True, suffix=f".{encoding}") as f:
        f.write(content)
        f.flush()

        if mode == "gs":
            client = storage.Client()
            bucket = client.get_bucket(settings.GS_MASTER_BUCKET, timeout=300.0)
            blob = bucket.blob(path)
            # NOTE: we upload via name instead of file object to 'detect' content type
            blob.upload_from_filename(f.name)

            update = {
                "encoding": encoding,
                "size": blob.size,
                "content_type": blob.content_type,
                "md5_hash": blob.md5_hash,
            }

        if mode == "fs":
            master_dir = settings.PROJECT_ROOT / "data" / "master" / f"{master.uid}"
            filename = master_dir / f"master.{encoding}"

            os.makedirs(master_dir, exist_ok=True)

            shutil.copy(f.name, filename)

            update = {
                "encoding": encoding,
                "size": os.path.getsize(f.name),
                "md5_hash": hashlib.md5(f.read()).hexdigest(),  # NOQA: S324
            }

            try:
                if content_type := mimetypes.guess_type(f.name)[0]:
                    update["content_type"] = content_type
            except KeyError:
                pass

    type(master).objects.filter(id=master.id).update(**update)

    logger.info(f"sync completed for {master.ct}:{master.uid}")

    return master
