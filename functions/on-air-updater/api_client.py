import json
import requests
from datetime import datetime, timedelta

URL = "https://openbroadcast.ch/api/v1/broadcast/schedule/"


class ApiError(Exception):
    pass


def get_metadata(timeshift=0):
    url = URL + "?secondsAhead=1800"
    try:
        r = requests.get(
            url,
            headers={
              "X-No-Cache": "1"
            },
            timeout=(2, 20)
        )
    except requests.exceptions.RequestException as e:
        raise ApiError(str(e)) from e

    if not r.status_code == 200:
        raise ApiError(f"unexpected status code {r.status_code}")

    try:
        data = r.json()
    except json.decoder.JSONDecodeError as e:
        raise ApiError(str(e)) from e

    if not isinstance(data, list):
        raise ApiError(f"unexpected result type {type(data)}")

    if not len(data):
        raise ApiError("empty result")

    now = datetime.now(tz=datetime.now().astimezone().tzinfo) - timedelta(seconds=timeshift)
    print(f"now shifted: {now:%H:%M:%S}")

    try:
        result = next(
            (
                i
                for i in data
                if datetime.fromisoformat(i["timeStart"])
                < now
                <= datetime.fromisoformat(i["timeEnd"])
            ),
            {},
        )
    except ValueError as e:
        raise ApiError(str(e)) from e
    
    if not "key" in result:
        raise ApiError(f"invalid result: {result}")

    try:
        dt = datetime.fromisoformat(result["timeEnd"])
        next_start_in = (dt - datetime.now(tz=dt.tzinfo)).total_seconds() + timeshift
    except ValueError as e:
        raise ApiError(str(e)) from e

    ts = datetime.fromisoformat(result["timeStart"])
    te = datetime.fromisoformat(result["timeEnd"])
    title = result["media"]["name"]
    print(f"runs:        {ts:%H:%M:%S} - {te:%H:%M:%S}     # {title}")

    return next_start_in, result


if __name__ == "__main__":
    next_start_in, result = get_metadata(timeshift=0)
    next_start_in_shifted, result_shifted = get_metadata(timeshift=-60)
    print("next_start_in:        ", next_start_in)
    print("next_start_in shifted:", next_start_in_shifted)
    # print(result, next_start_in)
