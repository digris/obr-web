import environ

from .base import *


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

GEOLOCATION_COUNTRY_OVERRIDE = "CH"

STREAMING_SERVICES_SPOTIFY_SOCIAL_AUTH_EMAIL = "none@none.no"


MEDIA_ROOT = PROJECT_ROOT / "data" / "media"
MEDIA_URL = ""

IMAGE_RESIZER_ENDPOINT = f"{SITE_URL}/images/"

MEDIA_ENDPOINTS = {
    "dash": f"{SITE_URL}/encoded/",
    "hls": f"{SITE_URL}/encoded/",
}

INSTALLED_APPS += [
    "dev",
]

MIDDLEWARE += []

CSRF_TRUSTED_ORIGINS = [
    "http://local.obr-next:3000",
    "http://local.obr-next:5000",
    "http://local.obr-next:8080",
    "http://localhost:5000",
    "http://localhost:8080",
]

if SITE_URL not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(SITE_URL)

MIDDLEWARE += [
    # "querycount.middleware.QueryCountMiddleware",
]

QUERYCOUNT = {
    "THRESHOLDS": {
        "MEDIUM": 50,
        "HIGH": 200,
        "MIN_TIME_TO_LOG": 0,
        "MIN_QUERY_COUNT_TO_LOG": 0,
    },
    "IGNORE_REQUEST_PATTERNS": [
        r"^/admin/jsi18n/",
        r"^/favicon.ico",
    ],
    "IGNORE_SQL_PATTERNS": [],
    "DISPLAY_DUPLICATES": 3,
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count",
}

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
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "streaming_services": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "donation": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
