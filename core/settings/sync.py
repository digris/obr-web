from .development import *

SITE_URL = "http://local.next.openbroadcast.ch:3000"

DEBUG = True

LANGUAGE_CODE = "en"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ch-openbroadcast",
        "HOST": "127.0.0.1",
        "PORT": 5433,
        "USER": "ch-openbroadcast",
        "PASSWORD": "bTEQe2WXtyFQsERyYIPPy900Iuhstj",
    },
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
}

# either
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "src"),
] + STATICFILES_DIRS


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


INSTALLED_APPS += []

MIDDLEWARE += []


STREAM_ENDPOINTS = {
    "dash": "https://stream-abr.next.openbroadcast.ch/stream.mpd",
    "hls": "https://stream-abr.next.openbroadcast.ch/manifest.m3u8",
    "icecast": "https://stream.next.openbroadcast.ch/256.mp3",
}

MEDIA_ENDPOINTS = {
    # "dash": "http://local.media.next.openbroadcast.ch:9090/encoded/",
    "dash": "/encoded/",
    "hls": "",
}

# MEDIA_ROOT = PROJECT_ROOT / "media"
# MEDIA_URL = "/media/"

DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = "ch-openbroadcast-media"
GS_DEFAULT_ACL = "publicRead"

##################################################################
# OBP API
##################################################################
OBP_SYNC_ENDPOINT = "https://www.openbroadcast.org/api/v2/obr-sync/"
OBP_SYNC_TOKEN = "c43108c1a98d073b69b4b8dab55e25169e88057b"
OBP_SYNC_DEBUG = False

OBP_SYNC_SKIP_MEDIA = False
OBP_SYNC_SKIP_IMAGES = False

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {
        "default": {"format": "%(levelname)s %(module)s %(message)s"},
        "verbose": {
            "format": "%(asctime)s %(levelname)s\t%(name)s\t%(funcName)s:%(lineno)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
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
        "django.request": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "account": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "user_identity": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "geoip": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sync": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "catalog": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "broadcast": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "subscription": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
