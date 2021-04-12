from .base import *

INTERNAL_IPS = ("127.0.0.1",)

DEBUG = True

SITE_URL = "http://next.openbroadcast.ch:3000"

##################################################################
# db
##################################################################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ch_openbroadcast_next_local",
        "USER": "",
        "HOST": "",
    },
}

# TEMPLATES[0]["OPTIONS"]["loaders"] = [
#     "django.template.loaders.filesystem.Loader",
#     "django.template.loaders.app_directories.Loader",
# ]

DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


##################################################################
# cache
##################################################################
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    # 'default': {
    #     'BACKEND': 'django_redis.cache.RedisCache',
    #     'LOCATION': 'redis://127.0.0.1:6379/7',
    #     'OPTIONS': {
    #         'CLIENT_CLASS': 'django_redis.client.DefaultClient',
    #     },
    # },
}

# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_CACHE_ALIAS = 'default'


##################################################################
# email
##################################################################
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = ''
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

INSTALLED_APPS += [
    # "dev",
    # 'debug_toolbar',
    # "django_extensions",
]

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# DEBUG_TOOLBAR_PANELS = [
#     #'cachalot.panels.CachalotPanel',
# ]

# this fixes strange behaviour when running app through gunicorn
DEBUG_TOOLBAR_PATCH_SETTINGS = False


WERKZEUG_DEBUG_PIN = "off"

DEVSERVER_MODULES = []

IPYTHON_ARGUMENTS = ["--debug"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {
        "default": {
            "format": "%(levelname)s %(name)s:%(lineno)s %(message)s",
        },
        "verbose": {
            # "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            "format": "%(asctime)s %(levelname)s\t%(name)s\t%(funcName)s:%(lineno)s - %(message)s",
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
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "geoip": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "catalog": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sync": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "raven": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
