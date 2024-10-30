#! /usr/bin/env python3
import base64
import json
import logging
import os
import requests

USER_AGENT = "openbroadcast.ch - metadata updater/0.0.1"

CHANNEL_KEY = os.environ.get("CHANNEL_KEY")
API_TOKEN = os.environ.get("API_TOKEN")

assert CHANNEL_KEY, "CHANNEL_KEY not set"
assert API_TOKEN, "API_TOKEN not set"

API_URL = f"https://metadata.streamabc.net/metapush/{CHANNEL_KEY}/{API_TOKEN}"


def update_metadata(item):
    media = item.get("media")

    if not media:
        return

    duration = media["duration"] - item["fadeIn"] * 0.001 - item["cueOut"] * 0.001

    cover_url = None

    if releases := media.get("releases", []):
        if path := releases[0].get("image", {}).get("path"):
            cover_url = f"https://openbroadcast.ch/images/crop/800x800/{path}"

    payload = {
        "id": item["key"],
        "time": item["timeStart"],
        #
        "song": media["name"],
        "artist": media["artistDisplay"],
        # "album": media["releaseDisplay"],
        "duration": round(duration),
        #
        "separator": " - ",
    }

    if cover_url:
        payload["cover"] = cover_url

    print(json.dumps(payload, indent=2))

    try:
        r = requests.post(
            API_URL,
            json=payload,
            headers={
                "user-agent": USER_AGENT,
            },
            timeout=(2, 10),
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
    r = requests.get("https://openbroadcast.ch/api/v1/broadcast/schedule/")
    update_metadata(r.json()[0])
