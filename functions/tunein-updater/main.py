#! /usr/bin/env python3
import base64
import json
import logging
import os
import requests

USER_AGENT = "openbroadcast.ch - metadata updater/0.0.1"

API_URL = os.environ.get("API_URL", "http://air.radiotime.com/Playing.ashx")

PARTNER_ID = os.environ.get("PARTNER_ID")
PARTNER_KEY = os.environ.get("PARTNER_KEY")
STATION_ID = os.environ.get("STATION_ID")

assert API_URL, "API_URL not set"
assert PARTNER_ID, "PARTNER_ID not set"
assert PARTNER_KEY, "PARTNER_KEY not set"
assert STATION_ID, "STATION_ID not set"


def update_metadata(item):
    media = item.get("media")

    if not media:
        return

    params = {
        "partnerId": PARTNER_ID,
        "partnerKey": PARTNER_KEY,
        "id": STATION_ID,
        "title": media["name"],
        "artist": media["artistDisplay"],
        "album": media["releaseDisplay"],
    }

    try:
        r = requests.get(
            API_URL,
            params=params,
            headers={
                "user-agent": USER_AGENT,
            },
            timeout=(10, 10),
        )

        print(r.status_code, r.text.replace("\n", ""))

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
