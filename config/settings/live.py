import io

import environ
import google.auth
import sentry_sdk
from google.cloud import secretmanager
from sentry_sdk.integrations.django import DjangoIntegration

SETTINGS_NAME = "ch-openbroadcast-settings"

_, project = google.auth.default()
client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project}/secrets/{SETTINGS_NAME}/versions/latest"
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

env = environ.Env()
env.read_env(io.StringIO(payload))

from .base import *  # NOQA

SITE_URL = "https://openbroadcast.ch"

##################################################################
# make sure to add further setting overrides *after*
# importing .base
##################################################################


SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = ["*"]
DEBUG = env("DEBUG")
DATABASES = {"default": env.db()}

SECURE_SSL_REDIRECT = True


# storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
GS_DEFAULT_ACL = "publicRead"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_SPOTIFY_KEY = env("SOCIAL_AUTH_SPOTIFY_KEY")
SOCIAL_AUTH_SPOTIFY_SECRET = env("SOCIAL_AUTH_SPOTIFY_SECRET")

# EMAIL_TIMEOUT = 60
# EMAIL_HOST = "smtp.eu.mailgun.org"
# EMAIL_PORT = 587
# EMAIL_HOST_USER = "postmaster@mailgun.hazelfire.com"
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")

OBP_SYNC_ENDPOINT = env("OBP_SYNC_ENDPOINT")
OBP_SYNC_TOKEN = env("OBP_SYNC_TOKEN")

SENTRY_DSN = env("SENTRY_DSN")

from .gcp_logging import LOGGING  # NOQA

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        _experiments={
            "profiles_sample_rate": 1.0,
        },
    )
