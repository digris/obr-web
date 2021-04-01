import json
import time
import requests
from datetime import timedelta

from catalog.models import Artist, Media, MediaArtists

REMOTE_BASE_URL = "https://www.openbroadcast.org"
REMOTE_API_AUTH_TOKEN = "cf7af17ee20679e69a0e8fbd0cd7597cc821e71d"
REQUEST_HEADERS = {
    "User-Agent": "openbroadcast.ch",
    "Authorization": "Token {auth_token}".format(auth_token=REMOTE_API_AUTH_TOKEN),
}


def get_flattened_schedule(time_range=(-3600, 3600)):
    url = "{base_url}/api/v2/abcast/flattened-schedule/".format(
        base_url=REMOTE_BASE_URL
    )
    params = {"time_range": "{},{}".format(time_range[0], time_range[1])}
    r = requests.get(url, params=params, headers=REQUEST_HEADERS, verify=True)
    if not r.status_code == 200:
        log.warning("unable to load remote data: status: {}".format(r.status_code))
        return []

    return r.json()


def synch_to_catalog():

    schedule = get_flattened_schedule((-14400, 14400))

    item_urls = [f"{REMOTE_BASE_URL}{s['item']}" for s in schedule.get("objects", [])]

    for url in item_urls:

        time.sleep(2)

        r = requests.get(url, headers=REQUEST_HEADERS)
        data = r.json()
        print(json.dumps(data, indent=2))

        if data["mediatype"] == "jingle":
            print("skip jingle")
            continue

        if Media.objects.filter(uuid=data["uuid"]).exists():
            print("skip existing")
            continue

        m = Media(
            uuid=data["uuid"],
            name=data["name"],
            duration=timedelta(seconds=data["duration"]),
        )

        m.save()

        if data["artist"]:
            ad = data["artist"]
            try:
                a = Artist.objects.get(uuid=ad["uuid"])
            except Artist.DoesNotExist:
                a = Artist(
                    uuid=ad["uuid"],
                    name=ad["name"],
                )
                a.save()

            MediaArtists.objects.get_or_create(
                media=m,
                artist=a,
            )

    print("schedule", item_urls)

    pass
