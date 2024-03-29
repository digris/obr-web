import json
import logging

from django.conf import settings

import requests

SYNC_ENDPOINT = settings.OBP_SYNC_ENDPOINT
SYNC_TOKEN = settings.OBP_SYNC_TOKEN
SYNC_DEBUG_REQUESTS = getattr(settings, "OBP_SYNC_DEBUG_REQUESTS", False)

HEADERS = {
    "User-Agent": "openbroadcast.ch - API sync client/0.0.1",
    "Authorization": f"Token {SYNC_TOKEN}",
}

logger = logging.getLogger(__name__)


class APIClientError(Exception):
    pass


class APIClient404Error(APIClientError):
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
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
    except requests.exceptions.RequestException as e:
        raise APIClientError(f"error connecting: {e}") from e

    if r.status_code == 404:
        raise APIClient404Error(f"resource does not exist: {r.status_code}")

    if not r.status_code == 200:
        raise APIClientError(f"invalid status-code returned: {r.status_code}")

    if raw:
        logger.debug("returning raw response")
        return r

    try:
        result = r.json()
    except json.JSONDecodeError as e:
        raise APIClientError(f"error decoding JSON response: {e}") from e

    if SYNC_DEBUG_REQUESTS:
        print(
            json.dumps(
                {
                    "url": url,
                    "data": result,
                },
                indent=2,
            ),
        )

    return result
