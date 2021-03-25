from .base import *

DEBUG = True
TEST_MODE = True
LOGGING = {}
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "build")
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
