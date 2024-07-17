import environ

from .base import *

SITE_URL = "http://local.obr-next:3000"


##################################################################
# storage & media
##################################################################
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


MEDIA_ROOT = PROJECT_ROOT / "data" / "media"
MEDIA_URL = ""

MEDIA_ENDPOINTS = {
    "dash": "/encoded/",
    "hls": "/encoded/",
}

INSTALLED_APPS += [
    "dev",
]

MIDDLEWARE += []

CSRF_TRUSTED_ORIGINS = [
    "http://local.obr-next:3000",
    "http://local.obr-next:5000",
    "http://local.obr-next:8080",
    "http://mba.local:5000",
]

MIDDLEWARE += [
    # "querycount.middleware.QueryCountMiddleware",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "WARNING",
        "handlers": ["console"],
    },
    "formatters": {
        "default": {
            "format": "%(levelname)-8s %(name)s %(message)s",
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
        "django.server": {
            "level": "WARNING",
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
        "account": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "stats": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sync": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
