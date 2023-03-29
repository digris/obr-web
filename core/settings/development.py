import environ

from .base import *

SITE_URL = "http://local.obr-next:3000"


##################################################################
# storage & media
##################################################################
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
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
]

MIDDLEWARE += [
    # "querycount.middleware.QueryCountMiddleware",
]

SENTRY_DSN = "https://59f51513d6e749b385eb59576dc19f2c@o995176.ingest.sentry.io/5953969"

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        _experiments={
            "profiles_sample_rate": 1.0,
        },
    )

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
        "account": {
            "level": "INFO",
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
