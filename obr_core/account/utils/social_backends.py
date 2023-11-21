from django.conf import settings

from social_core.backends.utils import user_backends_data
from social_django.models import UserSocialAuth
from social_django.utils import Storage

BACKENDS = settings.AUTHENTICATION_BACKENDS

AUTH_BACKENDS = [
    "apple-id",
    "google-oauth2",
]

SYNC_BACKENDS = [
    "spotify",
    "deezer",
]


def get_backends_for_user(user):
    backends_data = user_backends_data(user, BACKENDS, Storage)

    auth_backends = [b for b in backends_data.get("backends", []) if b in AUTH_BACKENDS]
    sync_backends = [
        b for b in backends_data.get("not_associated", []) if b in SYNC_BACKENDS
    ]

    # NOTE: quick fix to have apple as first (required for app store submission)
    auth_backends.sort()

    backends = {
        "connected": backends_data.get("associated", []),
        "disconnected": backends_data.get("not_associated", []),
        "all": backends_data.get("backends", []),
        "auth": auth_backends,
        "sync": sync_backends,
    }

    return backends


def disconnect_backend_for_user(user, provider, uid):
    return UserSocialAuth.objects.get(
        user=user,
        provider=provider,
        uid=uid,
    ).delete()
