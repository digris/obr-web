from social_core.backends.utils import user_backends_data
from social_django.utils import Storage, BACKENDS
from social_django.models import UserSocialAuth


def get_backends_for_user(user):

    backends_data = user_backends_data(user, BACKENDS, Storage)

    backends = {
        "connected": backends_data.get("associated", []),
        "disconnected": backends_data.get("not_associated", []),
        "all": backends_data.get("backends", []),
    }

    return backends


def disconnect_backend_for_user(user, provider, uid):
    return UserSocialAuth.objects.get(
        user=user,
        provider=provider,
        uid=uid,
    ).delete()
