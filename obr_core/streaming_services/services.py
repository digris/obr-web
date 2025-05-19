import json
import logging

import account.models
import catalog.models

from .api_client import APIClientError, SpotifyAPIClient
from .models import SyncProvider, SyncSettings

logger = logging.getLogger(__name__)


def media_link_to_spotify(
    *,
    media: catalog.models.Media,
):
    logger.debug(f"link media to spotify: {media}")
    client = SpotifyAPIClient()

    try:
        result = client.lookup_media(
            name=media.name,
            artist_name=media.artist_display,
        )
    except APIClientError as e:
        logger.error(f"APIClientError: {e}")
        return

    print(json.dumps(result, indent=2))

    if not result:
        logger.debug("no result")
        return

    if uri := result.get("uri"):
        media.identifiers.update_or_create(
            scope="spotify",
            defaults={
                "value": uri,
            },
        )


def media_link_to_deezer(
    *,
    media: catalog.models.Media,
):
    logger.debug(f"link media to deezer: {media}")


def media_set_remote_identifiers(
    *,
    media: catalog.models.Media,
):

    logger.debug(f"set identifiers: {media}")

    if not media.identifiers.filter(scope="spotify").exists():
        media_link_to_spotify(media=media)
    else:
        logger.debug("identifier exists")

    if not media.identifiers.filter(scope="deezer").exists():
        media_link_to_deezer(media=media)


def remote_media_sync_all_from_for_user(
    *,
    user: account.models.User,
    provider: SyncProvider,
) -> None:
    logger.debug(f"Syncing all media FROM provider {provider} for user {user}")


def remote_media_sync_all_to_for_user(
    *,
    user: account.models.User,
    provider: SyncProvider,
) -> None:
    logger.debug(f"Syncing all media TO provider {provider} for user {user}")


def sync_settings_get_for_user(
    *,
    user: account.models.User,
    provider: SyncProvider | str,
) -> SyncSettings:

    provider = SyncProvider(provider) if isinstance(provider, str) else provider

    sync_settings, _ = SyncSettings.objects.get_or_create(
        user=user,
        provider=provider,
    )

    print("sync_settings", sync_settings, sync_settings.social_auth)

    return sync_settings
