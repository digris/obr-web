from .development import *

#######################################################################
# use this file to extend / override `settings.development`
#######################################################################
SITE_URL = "http://next.openbroadcast.ch:3000"

##################################################################
# db
##################################################################

DEBUG = True

LANGUAGE_CODE = "en"
# LANGUAGES = (("en", "English"), ("de", "Deutsch"))

# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "db.sqlite3",
    }
}

INSTALLED_APPS += [
    # 'debug_toolbar',
]

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]
