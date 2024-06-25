import logging

from django.conf import settings

from account.models import User
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token

CLIENT_ID = settings.GOOGLE_AUTH_CLIENT_ID

SOCIAL_AUTH_PROVIDER = "google-oauth2"


logger = logging.getLogger(__name__)


class IdTokenLoginError(Exception):
    pass


def get_or_create_user(request, token):
    logger.debug(f"initiate google id-token login: {token}")

    try:
        id_data = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except GoogleAuthError as e:
        raise IdTokenLoginError(f"auth error: {e}") from e

    if id_data["aud"] != CLIENT_ID:
        raise IdTokenLoginError("invalid token audience.")

    user_created = False
    social_auth_uid = id_data["sub"]
    email = id_data["email"]
    first_name = id_data.get("given_name", "")
    last_name = id_data.get("family_name", "")

    try:
        user = User.objects.get(
            social_auth__provider=SOCIAL_AUTH_PROVIDER,
            social_auth__uid=social_auth_uid,
        )
        logger.info(
            f"got existing social-auth user: {user} - social-auth uid: {social_auth_uid}",
        )
        return user, user_created
    except User.DoesNotExist:
        pass

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            country=request.geolocation_country or "",
        )
        user.set_unusable_password()
        user.save()
        user_created = True

    if not user.social_auth.filter(
        provider=SOCIAL_AUTH_PROVIDER,
        uid=social_auth_uid,
    ).exists():
        logger.info(
            f"create social auth for: {user} - social-auth uid: {social_auth_uid}",
        )
        user.social_auth.create(
            user=user,
            provider=SOCIAL_AUTH_PROVIDER,
            uid=social_auth_uid,
        )

    return user, user_created
