from .development import *

##################################################################
# use this file to extend / override `settings.development`
##################################################################

SITE_URL = "http://local.next.openbroadcast.ch:3000"

DEBUG = True

LANGUAGE_CODE = "en"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "data" / "db" / "ch-openbroadcast-local",
    },
    "postgres": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ch-openbroadcast-local",
        "USER": "",
        "HOST": "",
    },
    # access live database via ./bin/sql_proxy
    "live": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ch-openbroadcast",
        "HOST": "127.0.0.1",
        "PORT": 5433,
        "USER": "ch-openbroadcast",
        "PASSWORD": "***",
    },
}

# either
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "src"),
] + STATICFILES_DIRS

# or
# STATICFILES_DIRS = [
#     os.path.join(PROJECT_ROOT, "src"),
# ]
# STATIC_ROOT = os.path.join(PROJECT_ROOT, "build")


INSTALLED_APPS += [
    "dev",
]

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # "querycount.middleware.QueryCountMiddleware",
]


STREAM_ENDPOINTS = {
    "dash": "https://stream-abr.next.openbroadcast.ch/stream.mpd",
    "hls": "https://stream-abr.next.openbroadcast.ch/manifest.m3u8",
    "icecast": "https://stream.next.openbroadcast.ch/256.mp3",
}

MEDIA_ENDPOINTS = {
    "dash": "http://local.media.next.openbroadcast.ch:9090/encoded/",
    "hls": "",
}

# storage via django-storages[google]
GS_BUCKET_NAME = "ch-openbroadcast-media"
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_DEFAULT_ACL = "publicRead"

SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SESSION_COOKIE_SAMESITE = None

##################################################################
# payments
##################################################################
STRIPE_PUBLISHABLE_KEY = "pk_test_51ItZA8ER2E1HdLWsOqnZR9NWZA8DGYHwcTxxFzjcVB0gbc4Pv048o6S8bOgFCJUd7lFXtXf6xdFwU2xejnTFvlsC00SuGvJ4G1"
STRIPE_SECRET_KEY = "***"

##################################################################
# OBP API (platform API to sync content from)
##################################################################
OBP_SYNC_ENDPOINT = "https://www.openbroadcast.org/api/v2/obr-sync/"
OBP_SYNC_TOKEN = "***"  # https://www.openbroadcast.org/admin/authtoken/token/
OBP_SYNC_DEBUG = False

OBP_SYNC_SKIP_MEDIA = True
