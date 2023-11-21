from django.conf import settings

from config import __version__

SHORT_SHA = getattr(settings, "GIT_SHORT_SHA", "")


def get_version():
    return str(__version__)


def get_short_sha():
    return SHORT_SHA
