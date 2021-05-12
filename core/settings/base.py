import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_ROOT = os.path.join(PROJECT_ROOT, "core")

sys.path.insert(0, APP_ROOT)


DEBUG = False

ALLOWED_HOSTS = ["*"]
SECRET_KEY = "-$0%!u7!*wouhr*-ofna8-zmswjp8l%q1(%1l9-n=&7z36@352"
SESSION_COOKIE_NAME = "sid"

SITE_URL = ""

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "django_filters",
    "social_django",
    "adminsortable2",
    "base",
    "api_extra",
    "sync",
    "account",
    "rating",
    "broadcast",
    "catalog",
    "electronic_mail",
    # "django_cleanup.apps.CleanupConfig",  # NOTE: this app has to be placed last
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "user_identity.middleware.UserIdentityMiddleware",
    # "request_logging.middleware.LoggingMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "geolocation.middleware.GeolocationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(APP_ROOT, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django_settings_export.settings_export",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "geolocation.context_processors.geolocation",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


##################################################################
# authentication
##################################################################
AUTH_USER_MODEL = "account.User"
LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    # "axes.backends.AxesBackend",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.spotify.SpotifyOAuth2",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
]

# social auth
SOCIAL_AUTH_POSTGRES_JSONFIELD = False
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "account.social_auth_pipeline.user_groups.add_user_to_team",
    "account.social_auth_pipeline.user_details.get_user_details",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

# google oauth2
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# https://developer.spotify.com/documentation/general/guides/scopes/
SOCIAL_AUTH_SPOTIFY_SCOPE = [
    "user-read-private",
    "user-read-email",
    "user-top-read",
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = False
USE_TZ = True

DATETIME_FORMAT = "Y-m-d H:i:sO"
DATE_FORMAT = "Y-m-d"


##################################################################
# static files
##################################################################
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# `build` -> webpack output
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "build"),
]

# 'dist' -> ./manage.py collectstatic output
STATIC_ROOT = os.path.join(PROJECT_ROOT, "dist")

# simply served via `django.views.static.serve` - then cached on CDN / LB
STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


##################################################################
# security & co
##################################################################
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
X_FRAME_OPTIONS = "SAMEORIGIN"


##################################################################
# file upload
##################################################################
# avoid in-memory files (as we need fs access)
FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

# MAX_UPLOAD_SIZE = 256MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 268435456


##################################################################
# API
##################################################################
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "api_extra.utils.api_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}

SWAGGER_SETTINGS = {
    "DEFAULT_AUTO_SCHEMA_CLASS": "api_extra.schema.AutoSchema",
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "`Authorization: Token <api_token>`",
        },
    },
}

# CORS_ORIGIN_ALLOW_ALL = True
# CORS_URLS_REGEX = r"^/api/.*$"
# CORS_ALLOW_METHODS = [
#     "OPTIONS",
#     "GET",
# ]

GRAPHENE = {
    "SCHEMA": "core.schema.schema",
}


##################################################################
# services
##################################################################
IMAGE_RESIZER_URL = "https://next.openbroadcast.ch/images/"
GOOGLE_TAG_ID = ""
STREAM_ENDPOINTS = {
    "dash": "https://stream-abr.next.openbroadcast.ch/stream.mpd",
    "hls": "",
    "icecast": "",
}
MEDIA_ENDPOINTS = {
    "dash": "https://media.next.openbroadcast.ch/encoded/",
    "hls": "",
}


##################################################################
# exported settings
##################################################################
SETTINGS_EXPORT = [
    "DEBUG",
    "SITE_URL",
    "STATIC_URL",
    "IMAGE_RESIZER_URL",
    "STREAM_ENDPOINTS",
    "MEDIA_ENDPOINTS",
]

##################################################################
# logging
##################################################################
LOGGING_ = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "WARNING", "handlers": ["console"]},
    "formatters": {
        "default": {"format": "%(levelname)s %(module)s %(message)s"},
        "verbose": {
            "format": "%(asctime)s %(levelname)s\t%(name)s\t%(funcName)s:%(lineno)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
        # "django.request": {
        #     "level": "DEBUG",
        #     "handlers": ["console"],
        #     "propagate": False,
        # },
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
