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

    def try_get_media():
        isrc = media.identifiers.filter(scope="isrc").first()
        if isrc:
            try:
                return client.get_media_by_isrc(isrc=isrc.value)
            except APIClientError as e:
                logger.error(f"APIClientError (ISRC): {e}")
        try:
            return client.get_media_by_search(
                name=media.name,
                artist_name=" ".join(ma.artist.name for ma in media.media_artist.all()),
            )
        except APIClientError as e:
            logger.error(f"APIClientError (Search): {e}")
        return None

    result = try_get_media()
    if not result:
        logger.debug("no result")
        return None

    uri = result.get("uri")
    if not uri:
        return None

    identifier, _ = media.identifiers.update_or_create(
        scope="spotify",
        defaults={"value": uri},
    )
    return identifier


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
