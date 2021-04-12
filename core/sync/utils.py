# -*- coding: utf-8 -*-
import json
import logging
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError

from broadcast.models import Emission
from catalog.models.playlist import Playlist

logger = logging.getLogger(__name__)

EMISSION_ENDPOINT = "https://www.openbroadcast.org/api/v2/abcast/emission/"


def fetch_emissions(start=None, end=None):

    fields = [
        "ct",
        "uuid",
        "time_start",
        "duration",
        "co.ct",
        "co.uuid",
        "co.name",
    ]

    limit = 200
    fields_str = ",".join(fields)

    url = f"{EMISSION_ENDPOINT}?limit={limit}&fields={fields_str}"

    if start:
        url += f"&time_start_0={start:%Y-%m-%d+%H:%M}"

    if end:
        url += f"&time_start_1={end:%Y-%m-%d+%H:%M}"

    next_page = url
    emissions = []
    while next_page:
        r = requests.get(url=next_page)

        data = r.json()
        # print(json.dumps(data, indent=2))
        next_page = data.get("next", None)
        results = data.get("results", [])
        emissions += results

    return emissions


def create_emission_objects(emission_list):
    for emission_dict in [e for e in emission_list if e.get("co")]:
        unaware_time_start = datetime.fromisoformat(emission_dict["time_start"])
        try:
            time_start = timezone.make_aware(unaware_time_start)
        except (AmbiguousTimeError, NonExistentTimeError):
            time_start = timezone.make_aware(unaware_time_start, is_dst=True)

        obj, _ = Emission.objects.get_or_create(uuid=emission_dict["uuid"])
        obj.time_start = time_start
        obj.obj_key = f"{emission_dict['co']['ct']}:{emission_dict['co']['uuid']}"
        obj.save()

        yield obj


def sync_schedule(date_start=None):

    schedule_ahead = 60 * 60 * 4  # 4 hours
    try:
        latest_emission = Emission.objects.filter(
            time_start__lte=timezone.now()
        ).latest()
    except Emission.DoesNotExist:
        latest_emission = None
    if latest_emission:
        start = timezone.make_naive(latest_emission.time_start)
        start = start if start > date_start else date_start
    elif date_start:
        start = date_start
    else:
        start = datetime(year=2000, month=1, day=1)

    end = datetime.now() + timedelta(seconds=schedule_ahead)

    logger.debug(f"fetch emissions from {start:%Y-%m-%d %H:%M} to {end:%Y-%m-%d %H:%M}")

    emission_list = fetch_emissions(start=start, end=end)

    for emission in create_emission_objects(emission_list):

        playlist_uuid = emission.obj_key.split(":")[1]

        try:
            playlist = Playlist.objects.get(uuid=playlist_uuid)

        except Playlist.DoesNotExist:
            playlist = Playlist(uuid=playlist_uuid, name="--init--")
            playlist.save()

        if emission.playlist_id != playlist.id:
            emission.playlist = playlist
            emission.save()

        yield emission
