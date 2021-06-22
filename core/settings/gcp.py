import io

import environ
import google.auth
from google.cloud import secretmanager

from .base import *  # NOQA

SITE_URL = "https://next.openbroadcast.ch"
SETTINGS_NAME = "ch-openbroadcast-settings"

_, project = google.auth.default()
client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project}/secrets/{SETTINGS_NAME}/versions/latest"
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

env = environ.Env(
    DEBUG=(bool, False),
)
env.read_env(io.StringIO(payload))


SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = ["*"]
DEBUG = env("DEBUG")
DATABASES = {"default": env.db()}

SECURE_SSL_REDIRECT = True


# storage via django-storages[google]
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# STATICFILES_STORAGE = "base.storage.StaticGCPStorage"
GS_DEFAULT_ACL = "publicRead"


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_SPOTIFY_KEY = env("SOCIAL_AUTH_SPOTIFY_KEY")
SOCIAL_AUTH_SPOTIFY_SECRET = env("SOCIAL_AUTH_SPOTIFY_SECRET")

EMAIL_TIMEOUT = 60
EMAIL_HOST = "smtp.eu.mailgun.org"
EMAIL_PORT = 587
EMAIL_HOST_USER = "postmaster@mailgun.hazelfire.com"
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

STRIPE_PUBLISHABLE_KEY = env("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY")


from .gcp_logging import LOGGING  # NOQA
