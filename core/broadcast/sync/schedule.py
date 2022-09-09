import logging
from datetime import datetime, timedelta

from django.utils import timezone
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError

from broadcast import signals as broadcast_signals
from broadcast.models import Emission
from catalog.models.playlist import Playlist
from sync import api_client

logger = logging.getLogger(__name__)


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
    limit = 200
    path = f"emissions/?limit={limit}"

    if start:
        path += f"&time_start_0={start:%Y-%m-%d+%H:%M}"

    if end:
        path += f"&time_start_1={end:%Y-%m-%d+%H:%M}"

    next_page = path
    emissions = []
    while next_page:
        try:
            data = api_client.get(path=next_page)
            next_page = data.get("next", None)
            results = data.get("results", [])
            emissions += results
        except api_client.APIClientException as e:
            logger.error(f"unable to get data: {e}")
            next_page = None

    return sorted(emissions, key=lambda emission: emission["time_start"])
    # return emissions


def create_emission_objects(emission_list):
    for emission_dict in [e for e in emission_list if e.get("co")]:
        time_start = parse_datetime(emission_dict["time_start"])
        time_end = round_datetime(parse_datetime(emission_dict["time_end"]), 60 * 5)

        obj, obj_created = Emission.objects.get_or_create(uuid=emission_dict["uuid"])
        obj.time_start = time_start
        obj.time_end = time_end
        obj.obj_key = f"{emission_dict['co']['ct']}:{emission_dict['co']['uuid']}"
        obj.save()

        verb = "created" if obj_created else "updated"
        logger.info(
            f"{verb} emission {obj.uid}: {time_start:%Y-%m-%d %H:%M} - {time_end:%Y-%m-%d %H:%M} "
        )

        yield obj


# pylint: disable=unused-argument
def sync_schedule(date_start=None, date_end=None, force=False, skip_media=False):
    if force:
        if not (date_start and date_end):
            raise Exception("required 'date_start' and 'date_end' when using 'force'")
        start = date_start
    else:
        try:
            latest_emission = Emission.objects.filter(
                time_start__lte=timezone.now()
            ).latest()
        except Emission.DoesNotExist:
            latest_emission = None
        if latest_emission:
            start = latest_emission.time_start
            if timezone.is_aware(start):
                start = timezone.make_naive(start)
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
        schedule_ahead = 60 * 60 * 24  # 24 hours
        end = datetime.now() + timedelta(seconds=schedule_ahead)

    logger.debug(f"fetch emissions from {start:%Y-%m-%d %H:%M} to {end:%Y-%m-%d %H:%M}")

    # return []

    emission_list = fetch_emissions(start=start, end=end)

    processed_emissions = []

    for emission in create_emission_objects(emission_list):

        playlist_uuid = emission.obj_key.split(":")[1]

        try:
            playlist = Playlist.objects.get(uuid=playlist_uuid)

        except Playlist.DoesNotExist:
            playlist = Playlist(uuid=playlist_uuid, name="-")
            playlist.save()

        if emission.playlist_id != playlist.id:
            emission.playlist = playlist
            emission.save()

        processed_emissions.append(emission)

    logger.debug(f"created {len(processed_emissions)} emissions")
    broadcast_signals.schedule_updated.send(
        sender=None,
        time_start=start,
        time_end=end,
        emissions=processed_emissions,
    )

    return processed_emissions
