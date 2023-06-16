import logging

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from account.models import User
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token

CLIENT_ID = settings.GOOGLE_AUTH_CLIENT_ID


logger = logging.getLogger(__name__)


class IdTokenValidationError(Exception):
    pass


class IdTokenLoginError(Exception):
    pass


def validate_id_token(token):
    logger.debug(f"initiate id-token login: {token}")

    try:
        id_data = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except GoogleAuthError as e:
        raise IdTokenValidationError(f"Auth error: {e}") from e

    try:
        print(id_data)
        return id_data
    except ValueError as e:
        raise IdTokenValidationError(_("Invalid token")) from e


def get_or_create_user(request, token):
    logger.debug(f"initiate id-token login: {token}")

    try:
        id_data = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except GoogleAuthError as e:
        raise IdTokenLoginError(f"Auth error: {e}") from e

    email = id_data["email"]
    first_name = id_data.get("given_name", "")
    last_name = id_data.get("family_name", "")

    user_created = False
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

    # NOTE: this is just a temporary solution... ;)
    if not user.social_auth.filter(provider="google-oauth2").exists():
        logger.info(f"create dummy social auth for: {user}")
        user.social_auth.create(
            user=user,
            provider="google-oauth2",
            uid=user.email,
        )

    return user, user_created
