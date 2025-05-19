import json
import time
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

import requests
from social_django.models import UserSocialAuth
from social_django.utils import load_strategy

SPOTIFY_SOCIAL_AUTH_EMAIL = settings.STREAMING_SERVICES_SPOTIFY_SOCIAL_AUTH_EMAIL


class APIClientError(Exception):
    pass


class SpotifyAPIClient:

    social_auth_provider = "spotify"
    social_auth_email = SPOTIFY_SOCIAL_AUTH_EMAIL
    base_url = "https://api.spotify.com/v1"

    def __init__(self): ...

    def get_access_token(self):
        try:
            sa = UserSocialAuth.objects.get(
                user__email=self.social_auth_email,
                provider=self.social_auth_provider,
            )
        except UserSocialAuth.DoesNotExist as e:
            raise APIClientError(
                f"UserSocialAuth not found: {self.social_auth_provider} - {self.social_auth_email} - {e}",
            ) from e

        # spotify auth does not include 'expires'. we check when the token was last updated
        # and "manually" refresh if older than 30 minutes (token valid for 1 hour)
        if sa.modified < timezone.now() - timedelta(seconds=30 * 60):
            print("refreshing token")
            sa.refresh_token(strategy=load_strategy())

        return sa.access_token

    def get_headers(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        return headers

    def get(self, path: str, params: dict = None) -> dict:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = self.get_headers()

        try:
            r = requests.get(url, params=params, headers=headers, timeout=(5, 30))

            if r.status_code == 429:
                print("Rate limit exceeded, sleep for 10 seconds...")
                time.sleep(10)

            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTPError", e)
            raise APIClientError(f"HTTP error: {e}") from e

        try:
            data = r.json()
        except json.decoder.JSONDecodeError as e:
            raise APIClientError(f"JSON decode error: {e}") from e

        return data

    def get_media_by_id(self, media_id: str) -> dict | None: ...

    def get_media_by_isrc(self, isrc: str) -> dict | None:

        query = f"isrc:{isrc}"

        params = {
            "q": query,
            "type": "track",
        }

        data = self.get("/search", params=params)

        tracks = data.get("tracks", {}).get("items", [])

        return tracks[0] if tracks else None

    def get_media_by_search(self, name: str, artist_name: str) -> dict | None:

        query = f"track:{name} artist:{artist_name}"

        params = {
            "q": query,
            "type": "track",
        }

        data = self.get("/search", params=params)

        tracks = data.get("tracks", {}).get("items", [])

        return tracks[0] if tracks else None


"""
headers = {"Authorization": f"Bearer {token}"}
"""
