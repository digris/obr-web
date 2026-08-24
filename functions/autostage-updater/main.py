#! /usr/bin/env python3
import base64
import json
import logging
import os
import requests

from datetime import datetime, timezone, timedelta

USER_AGENT = "openbroadcast.ch - metadata updater/0.0.1"

# https://onair.radioapi.io/ingest/digrisag/openbroadcast?format=radioapi&key=***&cid=***

API_URL = os.environ.get("API_URL", "https://onair.radioapi.io/ingest/digrisag/openbroadcast")
API_KEY = os.environ.get("API_KEY")
API_CID = os.environ.get("API_CID")

assert API_URL, "API_URL not set"
assert API_KEY, "API_KEY not set"
assert API_CID, "API_CID not set"

def get_duration(item):
    time_start = datetime.fromisoformat(item["timeStart"])
    time_end = datetime.fromisoformat(item["timeEnd"])

    duration = time_end - time_start

    total_seconds = int(duration.total_seconds())

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def format_timestamp(value):
    dt = datetime.fromisoformat(value)
    dt = dt.astimezone(timezone.utc)

    # we send from trigger 60s before start, so accordingly adjust the timestamp to be accordingly later
    # dt += timedelta(seconds=60)

    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def update_metadata(item):

    media = item.get("media")

    if not media:
        return

    image_url = f"https://openbroadcast.ch/slides/slide/cover/catalog.media:{media['uid']}/640x480.jpg"

    payload = {
        "nowPlaying": [
            {
                "type": "song",
                "status": "playing",
                "title": media.get("name", ""),
                "artist": media.get("artistDisplay", ""),
                "time": format_timestamp(item["timeStart"]),
                "duration": get_duration(item),
                "imageUrl": image_url,
            }
        ]
    }

    params = {
        "format": "radioapi",
        "key": API_KEY,
        "cid": API_CID,
    }

    try:
        r = requests.post(
            API_URL,
            params=params,
            json=payload,
            headers={
                "user-agent": USER_AGENT,
            },
            timeout=(10, 10),
        )

        print(r.status_code, r.text)

    except requests.exceptions.RequestException as e:
        print(f"error: {e}")
        logging.warning(f"error: {e}")
        return


def run(event, context):
    if "data" not in event:
        print("payload missing")
        return "error"

    decoded = base64.b64decode(event["data"]).decode("utf-8")
    payload = json.loads(decoded)

    key = payload["key"]
    title = payload["media"]["name"]
    time_start = payload["timeStart"]

    print(f"{key} - {time_start} - {title}")

    update_metadata(item=payload)

    logging.info(f"{key} - {title}")
    return "OK"


if __name__ == "__main__":
    r = requests.get(
        "https://openbroadcast.ch/api/v1/broadcast/schedule/",
        headers={
            "X-No-Cache": "1"
        },
        )
    update_metadata(r.json()[0])
