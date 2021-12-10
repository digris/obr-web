from .base import *

DEBUG = True
TEST_MODE = True
LOGGING = {}
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "build")
MEDIA_ROOT = PROJECT_ROOT / "data" / "test" / "media"
DATABASES = {
    "null": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/dev/null",
    },
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "db-test.sqlite3",
    },
}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
OBP_SYNC_SKIP_ALL = True

CATALOG_ARTIST_MIN_NUM_MEDIA = 0
