import base64
import datetime
import logging
import time

import jwt
import requests
from account.models import User
from jwt.algorithms import RSAAlgorithm
from jwt.exceptions import PyJWTError

SOCIAL_AUTH_PROVIDER = "apple-id"

ID_TOKEN_ISSUER = "https://appleid.apple.com"  # noqa S105

APP_ID = "ch.digris.obrapp"
APP_TEAM_ID = "236JDQVAKF"

APP_KEY_ID = "DX7Z5X95D3"
APP_KEY_CONTENT = """-----BEGIN PRIVATE KEY-----
(( THIS IS NOT THE KEY ;) ))
-----END PRIVATE KEY-----"""


logger = logging.getLogger(__name__)


class AppleIdLoginError(Exception):
    pass


def base64_decode(value):
    value += "=" * (4 - (len(value) % 4))
    return base64.urlsafe_b64decode(value).decode()


def get_public_key(key_id):
    url = "https://appleid.apple.com/auth/keys"
    r = requests.get(url, timeout=5)
    keys = r.json()["keys"]
    return next((key for key in keys if key["kid"] == key_id), None)


def generate_client_secret():
    now = int(time.time())

    headers = {"kid": APP_KEY_ID}
    payload = {
        "iss": APP_TEAM_ID,
        "iat": now,
        "exp": now + 15552000,  # 6 months
        "aud": ID_TOKEN_ISSUER,
        "sub": APP_ID,
    }

    return jwt.encode(payload, key=APP_KEY_CONTENT, algorithm="ES256", headers=headers)


def verify_authorization_code(authorization_code):
    print("ac", authorization_code)

    client_secret = generate_client_secret()

    url = "https://appleid.apple.com/auth/token"

    payload = {
        "client_id": APP_ID,
        "client_secret": client_secret,
        "code": authorization_code,
        "grant_type": "authorization_code",
        "redirect_uri": "https://openbroadcast.ch/social/complete/apple-id/",
    }

    r = requests.post(
        url,
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        timeout=5,
    )

    print(r.status_code)
    print(r.text)


def decode_id_token(id_token):
    id_token = base64_decode(id_token)

    try:
        kid = jwt.get_unverified_header(id_token).get("kid")
        public_key = RSAAlgorithm.from_jwk(get_public_key(kid))
        decoded = jwt.decode(
            id_token,
            key=public_key,
            audience=APP_ID,
            algorithms=["RS256"],
        )
    except PyJWTError as e:
        raise AppleIdLoginError(f"token validation failed by {e}") from e

    return decoded


def get_or_create_user(  # noqa C901
    request,
    id_token,
    authorization_code,
    profile=None,
):
    payload = decode_id_token(id_token)
    print("payload", payload)

    issuer = payload.get("iss")
    audience = payload.get("aud")
    expires_at = payload.get("exp")
    email = payload.get("email")
    payload.get("email_verified")
    apple_id = payload.get("sub")

    if issuer != ID_TOKEN_ISSUER:
        raise AppleIdLoginError(f"invalid issuer: {issuer}")

    if audience != APP_ID:
        raise AppleIdLoginError(f"invalid audience: {audience}")

    if datetime.datetime.fromtimestamp(
        expires_at,
        tz=datetime.UTC,
    ) < datetime.datetime.now(
        tz=datetime.UTC,
    ):
        raise AppleIdLoginError("token has expired")

    # NOTE: this does not work at the moment:

    social_auth_uid = apple_id
    user_created = False

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
            country=request.geolocation_country or "",
        )

        if first_name := profile.get("given_name"):
            user.first_name = first_name

        if last_name := profile.get("family_name"):
            user.last_name = last_name

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
