import environ
from .base import *

SITE_URL = "http://local.next.openbroadcast.ch:3000"


##################################################################
# storage & media
##################################################################
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_ROOT = PROJECT_ROOT / "data" / "media"
MEDIA_URL = ""

INSTALLED_APPS += []

MIDDLEWARE += []

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
    "formatters": {
        "default": {
            "format": "%(levelname)-8s %(name)s\t%(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.request": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "geoip": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "catalog": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "sync": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
