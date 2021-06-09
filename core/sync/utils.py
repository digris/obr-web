# -*- coding: utf-8 -*-
import logging
from datetime import datetime, timedelta

import requests
from django.utils import timezone
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError

from broadcast.models import Emission
from catalog.models.playlist import Playlist

logger = logging.getLogger(__name__)

EMISSION_ENDPOINT = "https://www.openbroadcast.org/api/v2/abcast/emission/"


def parse_datetime(dt_str):
    """
    convert unaware datetime to aware.
    tries to fix times during DST transitions
    """
    unaware_time_start = datetime.fromisoformat(dt_str)
    try:
        dt = timezone.make_aware(unaware_time_start)
    except (AmbiguousTimeError, NonExistentTimeError):
        is_dst = timezone.localtime().dst()
        dt = timezone.make_aware(unaware_time_start, is_dst=is_dst)
    return dt


def round_datetime(dt=None, round_to=60):
    """
    round datetime time to nearest given seconds
    """
    seconds = (dt.replace(tzinfo=None) - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)


def fetch_emissions(start=None, end=None):

    fields = [
        "ct",
        "uuid",
        "time_start",
        "time_end",
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

        time_start = parse_datetime(emission_dict["time_start"])
        time_end = round_datetime(parse_datetime(emission_dict["time_end"]), 60 * 5)

        # print(json.dumps(emission_dict, indent=2))
        duration = emission_dict.get("duration")

        print(time_start, time_end, duration)

        obj, _ = Emission.objects.get_or_create(uuid=emission_dict["uuid"])
        obj.time_start = time_start
        obj.time_end = time_end
        obj.obj_key = f"{emission_dict['co']['ct']}:{emission_dict['co']['uuid']}"
        obj.save()

        yield obj


def sync_schedule(date_start=None, date_end=None, force=False):

    if force:
        if not date_start:
            raise Exception("required 'date_start' when using 'force'")
        start = date_start
    else:
        try:
            latest_emission = Emission.objects.filter(
                time_start__lte=timezone.now()
            ).latest()
        except Emission.DoesNotExist:
            latest_emission = None
        if latest_emission:
            start = timezone.make_naive(latest_emission.time_start)
            if date_start:
                start = start if start > date_start else date_start
        elif date_start:
            start = date_start
        else:
            start = datetime(year=2000, month=1, day=1)

    if date_end:
        end = date_end
        if end.hour == 0 and end.minute == 0:
            # looks like a bare date without time information
            end = end.replace(hour=23, minute=59, second=59)
    else:
        schedule_ahead = 60 * 60 * 4  # 4 hours
        end = datetime.now() + timedelta(seconds=schedule_ahead)

    logger.debug(f"fetch emissions from {start:%Y-%m-%d %H:%M} to {end:%Y-%m-%d %H:%M}")

    # return []

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