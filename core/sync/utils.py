import requests
import json
import time
from datetime import datetime, timedelta
from django.utils import timezone
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from broadcast.models import Emission
from catalog.models.playlist import Playlist, PlaylistImage

# EMISSION_ENDPOINT = "https://www.openbroadcast.org/api/v2/abcast/emission/?limit=500&fields=ct,uuid,url,co,name,series,image,time_start,time_end,duration,updated,color,has_lock,co.ct,co.uuid,co.name,co.url,co.duration&time_start_0=2021-03-29+06:00&time_start_1=2021-04-12+05:59"

EMISSION_ENDPOINT = "https://www.openbroadcast.org/api/v2/abcast/emission/"
PLAYLIST_ENDPOINT = "https://www.openbroadcast.org/api/v2/alibrary/playlist/"


def fetch_emissions(time_start=None, time_end=None):

    emissions = []
    url = EMISSION_ENDPOINT
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

    if time_start:
        url += f"&time_start_0={time_start}"

    if time_end:
        url += f"&time_start_1={time_end}"

    next = url
    while next:
        print("next", next)
        r = requests.get(url=next)

        data = r.json()
        results = data.get("results", [])
        next = data.get("next", None)
        # print(results)
        # print(next)

        emissions += results

        # next = False

    return emissions


def sync_schedule(date_start=None):
    print("sync schedule")

    schedule_ahead = 60 * 60 * 4  # 4 hours

    # latest emission (with start_time in past)
    try:
        latest_emission = Emission.objects.filter(
            time_start__lte=timezone.now()
        ).latest()
    except Emission.DoesNotExist:
        latest_emission = None
    if latest_emission:
        time_start = timezone.make_naive(latest_emission.time_start)
        if time_start < date_start:
            filter_time_start = date_start.strftime("%Y-%m-%d+%H:%M")
        else:
            filter_time_start = time_start.strftime("%Y-%m-%d+%H:%M")
    elif date_start:
        filter_time_start = date_start.strftime("%Y-%m-%d+%H:%M")
    else:
        filter_time_start = None

    filter_time_end = (datetime.now() + timedelta(seconds=schedule_ahead)).strftime(
        "%Y-%m-%d+%H:%M"
    )

    print(filter_time_start)
    print(filter_time_end)

    import sys

    # sys.exit(0)

    emissions = fetch_emissions(time_start=filter_time_start, time_end=filter_time_end)
    print(f"fetched {len(emissions)} emissions")
    # print(json.dumps(emissions, indent=2))

    emission_objects = []
    for e in emissions:

        if not e.get("co", None):
            print(json.dumps(e, indent=2))
            continue

        unaware_time_start = datetime.fromisoformat(e["time_start"])
        try:
            time_start = timezone.make_aware(unaware_time_start)
        except (AmbiguousTimeError, NonExistentTimeError):
            print("force DST")
            time_start = timezone.make_aware(unaware_time_start, is_dst=True)

        if not time_start:
            print(json.dumps(e, indent=2))
            continue

        obj, _ = Emission.objects.get_or_create(uuid=e["uuid"])
        obj.time_start = time_start
        obj.obj_key = f"{e['co']['ct']}:{e['co']['uuid']}"
        obj.save()
        emission_objects.append(obj)

    # print(emission_objects)

    print(f"created / updated {len(emission_objects)} emissions")

    for emission in Emission.objects.all():
        playlist_uuid = emission.obj_key.split(":")[1]
        playlist, created = Playlist.objects.get_or_create(uuid=playlist_uuid)
        if created:
            playlist.name = "--initial--"
            playlist.save()

        if emission.playlist_id != playlist.id:
            emission.playlist = playlist
            emission.save()


def sync_playlist(playlist):
    print(f"sync playlist: {playlist}")

    url = f"{PLAYLIST_ENDPOINT}{playlist.uuid}/"

    fields = [
        "uuid",
        "name",
        "image",
        "created",
        "updated",
    ]

    params = {"fields": ",".join(fields)}

    print(url)

    r = requests.get(url=url, params=params)

    data = r.json()

    print(json.dumps(data, indent=2))

    playlist.name = data.get("name")

    created = timezone.make_aware(datetime.fromisoformat(data.get("created")))
    playlist.created = created

    # updated = timezone.make_aware(datetime.fromisoformat(data.get("updated")))
    # playlist.updated = updated

    playlist.save()

    if data.get("image"):
        image_url = data.get("image")
        image_url = ".".join(b for b in image_url.split(".")[:-2]).replace(
            "thumbnails/", ""
        )

        ext = image_url.split(".")[-1]
        # filename = f"{playlist.uid}.{ext}"
        filename = f"downloaded-image.{ext}"

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()

        i = PlaylistImage(playlist=playlist)
        i.save()
        i.file.save(filename, File(img_temp))


def sync_playlists():
    print("sync playlists")
    qs = Playlist.objects.all()

    PlaylistImage.objects.all().delete()

    for playlist in qs[0:1000]:
        sync_playlist(playlist)
