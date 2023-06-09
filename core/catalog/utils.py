from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q

import google.auth
from base.utils.qs import next_in_order, prev_in_order  # pragma: no cover
from google.auth.transport import requests as auth_requests
from google.cloud import storage


def get_signed_master_url(master):
    seconds_valid = 15 * 60
    cache_key = f"master-url:{master.path}"

    if url := cache.get(cache_key):
        return url

    # in case of GCP storage: get signed url
    if settings.STORAGES["default"]["BACKEND"] == "storages.backends.gcloud.GoogleCloudStorage":
        # https://stackoverflow.com/questions/64234214
        credentials, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/iam"],
        )
        credentials.refresh(auth_requests.Request())

        client = storage.Client()
        bucket = client.get_bucket(settings.GS_MASTER_BUCKET)
        blob = bucket.blob(master.path)
        url = blob.generate_signed_url(
            version="v2",
            method="GET",
            expiration=timedelta(seconds=seconds_valid + 60),
            service_account_email=credentials.service_account_email,
            access_token=credentials.token,
        )

    # in case of local storage (development): get static url
    else:
        url = f"{settings.SITE_URL.rstrip('/')}/master/{master.path}"

    cache.set(cache_key, url, seconds_valid)

    return url


def get_surrounding_media(media):  # pragma: no cover
    preceding = []
    succeeding = []
    qs_pm = media.playlist_media.all()
    qs_pm = qs_pm.select_related(
        "playlist",
        "media",
    )
    qs_pm = qs_pm.prefetch_related(
        "playlist__playlist_media__media",
    )
    for playlist_media in qs_pm:
        qs = playlist_media.playlist.playlist_media
        # TODO: implement media type
        qs = qs.exclude(
            Q(media__name__icontains="jingle") | Q(media__name__icontains="station"),
        )

        pm = qs.get(position=playlist_media.position)
        previous = prev_in_order(pm, qs=qs)
        next_pm = next_in_order(pm, qs=qs)

        if previous and previous.media not in preceding:
            preceding.append(previous.media)

        if next_pm and next_pm.media not in succeeding:
            succeeding.append(next_pm.media)

    return preceding, succeeding
