#! /usr/bin/env python3
import base64
import json
import logging
import os
import requests

USER_AGENT = "openbroadcast.ch - metadata updater/0.0.1"
API_URL = os.environ.get("API_URL", "https://stream.openbroadcast.ch/")
API_TOKEN = os.environ.get("API_TOKEN")

assert API_URL, "API_URL not set"
assert API_TOKEN, "API_TOKEN not set"


def update_metadata(item):
    media = item.get("media")
    playlist = item.get("playlist")

    if not media:
        return

    payload = {
        "title": media["name"],
        "artist": media["artistDisplay"],
    }

    if series := playlist.get("series"):

        show = series.get("name")

        if episode := series.get("episode"):
            show += f" #{episode}"

        payload["show"] = show

    try:
        r = requests.post(
            API_URL + "metadata",
            json=payload,
            headers={
                "user-agent": USER_AGENT,
                "Authorization": f"Bearer {API_TOKEN}",
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
    r = requests.get("https://openbroadcast.ch/api/v1/broadcast/schedule/")
    update_metadata(r.json()[0])
