import json

from django.conf import settings

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

        return sa.get_access_token(strategy=load_strategy())

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
            response = requests.get(url, params=params, headers=headers, timeout=(1, 2))
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise APIClientError(f"HTTP error: {e}") from e

        try:
            data = response.json()
        except json.decoder.JSONDecodeError as e:
            raise APIClientError(f"JSON decode error: {e}") from e

        return data

    def lookup_media(self, name: str, artist_name: str) -> dict | None:

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
