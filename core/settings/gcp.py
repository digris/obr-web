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
