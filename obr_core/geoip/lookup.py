import json

import requests

BASE_URL = "https://json.geoiplookup.io/"


class GeoipError(Exception):
    pass


def geoip(ip):
    url = f"{BASE_URL}{ip}"

    try:
        r = requests.get(url, timeout=(1, 5))
    except requests.exceptions.RequestException as e:
        raise GeoipError(f"error connecting: {e}") from e

    if not r.status_code == 200:
        raise GeoipError(f"invalid status-code returned: {r.status_code}")

    try:
        result = r.json()
    except json.JSONDecodeError as e:
        raise GeoipError(f"error decoding JSON response: {e}") from e

    return result
