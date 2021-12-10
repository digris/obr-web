import json
import logging

import requests
from django.conf import settings

SYNC_ENDPOINT = getattr(settings, "OBP_SYNC_ENDPOINT")
SYNC_TOKEN = getattr(settings, "OBP_SYNC_TOKEN")
SYNC_DEBUG = getattr(settings, "OBP_SYNC_DEBUG", False)

HEADERS = {
    "User-Agent": "openbroadcast.ch - API sync client/0.0.1",
    "Authorization": f"Token {SYNC_TOKEN}",
}

logger = logging.getLogger(__name__)


class APIClientException(Exception):
    pass


def get_url(path):
    endpoint = f"{SYNC_ENDPOINT.rstrip('/')}/"
    path = path.replace(endpoint, "")
    if path.startswith(("http://", "https://")):
        return path
    return f"{endpoint}{path}"


def get(path, params=None, raw=False):
    if not params:
        params = {}
    url = get_url(path=path)
    logger.debug(f"{url} - {params}")
    try:
        r = requests.get(url, params=params, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        raise APIClientException(f"error connecting: {e}") from e

    if not r.status_code == 200:
        raise APIClientException(f"invalid status-code returned: {r.status_code}")

    if raw:
        logger.debug("returning raw response")
        return r

    try:
        result = r.json()
    except json.JSONDecodeError as e:
        raise APIClientException(f"error decoding JSON response: {e}") from e

    if SYNC_DEBUG:
        print(
            json.dumps(
                {
                    "url": url,
                    "data": result,
                },
                indent=2,
            )
        )

    return result
