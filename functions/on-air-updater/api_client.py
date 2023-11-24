import json
import requests
from datetime import datetime

URL = "https://next.openbroadcast.ch/api/v1/broadcast/schedule/"


class ApiError(Exception):
    pass


def get_metadata():
    try:
        r = requests.get(URL + "?secondsAhead=1800")
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

    now = datetime.now(tz=datetime.now().astimezone().tzinfo)
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

    print(result["key"])
    print(result["media"]["name"])

    try:
        dt = datetime.fromisoformat(result["timeEnd"])
        next_start_in = (dt - datetime.now(tz=dt.tzinfo)).total_seconds()
    except ValueError as e:
        raise ApiError(str(e)) from e

    return next_start_in, result


if __name__ == "__main__":
    next_start_in, result = get_metadata()
    print(result, next_start_in)
