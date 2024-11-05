import json

from django.conf import settings

import geoip2.database
import geoip2.errors
import requests

BASE_URL = "https://json.geoiplookup.io/"


DB_FILE = settings.PROJECT_ROOT / "data/geoip/GeoLite2-City.mmdb"


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


try:
    reader = geoip2.database.Reader(DB_FILE)
except FileNotFoundError:
    reader = None


def geoip_mm(ip):
    if not reader:
        raise GeoipError("unable to open GeoLite2 database")

    try:
        res = reader.city(ip)
    except geoip2.errors.AddressNotFoundError as e:
        raise GeoipError(f"unable to lookup: {e}") from e

    return {
        "city": res.city.name or "",
        "region": res.subdivisions.most_specific.name or "",
        "country_code": res.country.iso_code or "",
    }
