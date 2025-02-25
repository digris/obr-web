from .base import *  # NOQA

##################################################################
# make sure to add further setting overrides *after*
# importing .base
##################################################################

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
DATABASES = {"default": env.db()}

OBP_SYNC_ENDPOINT = env("OBP_SYNC_ENDPOINT")
OBP_SYNC_TOKEN = env("OBP_SYNC_TOKEN")

ALLOWED_HOSTS = ["*"]

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
