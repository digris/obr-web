import os
import sys
from datetime import timedelta
from pathlib import Path

import environ

from .. import __version__

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_ROOT = os.path.join(PROJECT_ROOT, "core")

sys.path.insert(0, APP_ROOT)

env = environ.Env(
    DEBUG=(bool, False),
    OBP_SYNC_SKIP_MEDIA=(bool, False),
    OBP_SYNC_SKIP_IMAGES=(bool, False),
)

DEBUG = env("DEBUG")
SECRET_KEY = env(
    "SECRET_KEY",
    default="---secret-key---",
)

ALLOWED_HOSTS = ["*"]
SESSION_COOKIE_NAME = "sid"
SESSION_COOKIE_SAMESITE = None

SITE_URL = ""

INSTALLED_APPS = [
    # "admin_interface",
    # "colorfield",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "storages",
    # "taggit",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_filters",
    "social_django",
    "django_countries",
    "adminsortable2",  # disabled for the moment. (wait for django 4 support)
    "base",
    "tagging",
    "api_extra",
    "sync",
    "account",
    "app_bridge",
    "user_identity",
    "subscription",
    "identifier",
    "rating",
    "broadcast",
    "catalog",
    "cms",
    "faq",
    "share",
    "redirect",
    "electronic_mail",
    "stats",
    "newsletter",
    "slack",
    #
    "usersnap",
    "django_cleanup.apps.CleanupConfig",  # NOTE: this app has to be placed last
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "vite.middleware.ViteProxiedMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "user_identity.middleware.UserIdentityMiddleware",
    # "request_logging.middleware.LoggingMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "geolocation.middleware.GeolocationMiddleware",
    "client_mode.middleware.ClientModeMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

APPEND_SLASH = True

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
                "vite.context_processors.vite_proxied",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django_settings_export.settings_export",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "base.context_processors.version",
                "geolocation.context_processors.geolocation",
                "client_mode.context_processors.client_mode",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


##################################################################
# db
##################################################################
DATABASES = {
    "default": env.db(
        default="postgres://obr:obr@db:5432/obr",
    ),
    "event": env.db_url(
        "EVENT_DATABASE_URL",
        default="sqlite:////dev/null",
    ),
    "sync": env.db_url(
        "SYNC_DATABASE_URL",
        default="sqlite:////dev/null",
    ),
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


##################################################################
# cache
##################################################################
CACHES = {
    "default": env.cache(
        default="dummycache://",
    ),
}


SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


##################################################################
# email
##################################################################
EMAIL_CONFIG = env.email(
    "EMAIL_URL",
    default="consolemail://",
)
vars().update(EMAIL_CONFIG)

DEFAULT_FROM_EMAIL = "open broadcast radio <no-reply@openbroadcast.ch>"


##################################################################
# authentication
##################################################################
AUTH_USER_MODEL = "account.User"
LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    # "axes.backends.AxesBackend",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.spotify.SpotifyOAuth2",
    "social_core.backends.apple.AppleIdAuth",
    "account.social_auth_backends.deezer.DeezerOAuth2",
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
    "account.social_auth_pipeline.app_bridge.app_redirect",
    "account.social_auth_pipeline.user_redirect.registration_redirect",
)

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

# keep track of originating call (used in app mode)
# https://python-social-auth.readthedocs.io/en/latest/use_cases.html#pass-custom-get-post-parameters-and-retrieve-them-on-authentication
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ["source"]

# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = "/account/settings/"

# google oauth2
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY",
    default="",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET",
    default="",
)


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

# deezer oauth2
SOCIAL_AUTH_DEEZER_KEY = env(
    "SOCIAL_AUTH_DEEZER_KEY",
    default="",
)

SOCIAL_AUTH_DEEZER_SECRET = env(
    "SOCIAL_AUTH_DEEZER_SECRET",
    default="",
)

SOCIAL_AUTH_DEEZER_SCOPE = [
    "manage_library",
    "listening_history",
    "manage_library",
    "offline_access",
]

# apple id
SOCIAL_AUTH_APPLE_ID_CLIENT = env(
    "SOCIAL_AUTH_APPLE_ID_CLIENT",
    default="",
)
SOCIAL_AUTH_APPLE_ID_TEAM = env(
    "SOCIAL_AUTH_APPLE_ID_TEAM",
    default="",
)
SOCIAL_AUTH_APPLE_ID_KEY = env(
    "SOCIAL_AUTH_APPLE_ID_KEY",
    default="",
)
SOCIAL_AUTH_APPLE_ID_SECRET = env.str(
    "SOCIAL_AUTH_APPLE_ID_SECRET",
    multiline=True,
    default="",
)
# SOCIAL_AUTH_APPLE_ID_SECRET = """
# -----BEGIN PRIVATE KEY-----
# MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgzxsOPmjnJ+/76BYe
# FMZGnuBRM/LWsvZe6hoxMiTMwROgCgYIKoZIzj0DAQehRANCAATN1pfGDwkN6NXQ
# uqcQR2R9RHnf7cnXveyOCTQIdZlPOBtgi1I0zAVS5fZ14RV7R4P57NrtY3VoACyZ
# ibVEjEBq
# -----END PRIVATE KEY-----"""
SOCIAL_AUTH_APPLE_ID_SCOPE = [
    "email",
    "name",
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", "English"),
    ("de", "Deutsch"),
    ("fr", "French"),
]

TIME_ZONE = "Europe/Zurich"
USE_I18N = True
USE_L10N = False
USE_TZ = True

DATETIME_FORMAT = "Y-m-d H:i:sO"
DATE_FORMAT = "Y-m-d"


##################################################################
# static files
##################################################################
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# `build` -> vite output
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

GS_BUCKET_NAME = env(
    "GS_BUCKET_NAME",
    default="",
)


##################################################################
# security & co
##################################################################
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
X_FRAME_OPTIONS = "SAMEORIGIN"


##################################################################
# localization & translation
##################################################################
LOCALE_PATHS = [os.path.join(APP_ROOT, "locale")]


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
# tagging
##################################################################
TAGGIT_CASE_INSENSITIVE = False


##################################################################
# API
##################################################################
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "api_extra.utils.api_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        # NOTE: do we need these parsers?
        # "djangorestframework_camel_case.parser.CamelCaseFormParser",
        # "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/minute",
        "user": "240/minute",
        "subscription.voucher": "10/hour",
        "account.login_email": "20/hour",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # 'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SIMPLE_JWT = {
    "USER_ID_FIELD": "uid",
    "USER_ID_CLAIM": "user_uid",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.SlidingToken",),
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=60 * 12),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=3),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "OBR API",
    "DESCRIPTION": "open broadcast radio",
    "VERSION": str(__version__),
    "SCHEMA_PATH_PREFIX": "/api/v[0-9]",
    "CAMELIZE_NAMES": True,
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_NO_READ_ONLY_REQUIRED": True,
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": False,
    # 'PREPROCESSING_HOOKS': [],
    "SORT_OPERATIONS": True,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
    "SERVERS": [
        {
            "url": "https://next.openbroadcast.ch",
        },
        {
            "url": "http://local.obr-next:8080",
        },
    ],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": False,
        "persistAuthorization": True,
        "displayOperationId": False,
        "defaultModelsExpandDepth": 100,
        "defaultModelExpandDepth": 100,
        # "docExpansion": "full",
    },
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@4.17.1",
    # https://drf-spectacular.readthedocs.io/en/latest/faq.html
    # look for "Enum names"
    "ENUM_NAME_OVERRIDES": {
        "VoteSourceEnum": "rating.models.VoteSource.choices",
        "VoteScopeEnum": "rating.models.VoteScope.choices",
    },
}


##################################################################
# services
##################################################################
STREAM_ENDPOINTS = {
    "dash": "https://stream-abr.next.openbroadcast.ch/dash/stream.mpd",
    "hls": "https://stream-abr.next.openbroadcast.ch/hls/manifest.m3u8",
    "icecast": "https://stream.next.openbroadcast.ch/256.mp3",
}

STREAM_LATENCY = 32.5  # seconds

MEDIA_ENDPOINTS = {
    "dash": "https://media.next.openbroadcast.ch/encoded/",
    "hls": "https://media.next.openbroadcast.ch/encoded/",
}

IMAGE_RESIZER_ENDPOINT = env(
    "IMAGE_RESIZER_ENDPOINT",
    default="https://next.openbroadcast.ch/images/",
)


##################################################################
# context
##################################################################
GIT_SHORT_SHA = env(
    "GIT_SHORT_SHA",
    default="",
)


##################################################################
# payment providers
##################################################################
STRIPE_PUBLISHABLE_KEY = env(
    "STRIPE_PUBLISHABLE_KEY",
    default="",
)
STRIPE_SECRET_KEY = env(
    "STRIPE_SECRET_KEY",
    default="",
)


##################################################################
# analytics
##################################################################
GOOGLE_GTM_ID = env(
    "GOOGLE_GTM_ID",
    default="GTM-KXBKVVT",
)


##################################################################
# exported settings
##################################################################
SETTINGS_EXPORT = [
    "DEBUG",
    "SITE_URL",
    "STATIC_URL",
    "IMAGE_RESIZER_ENDPOINT",
    "STREAM_ENDPOINTS",
    "MEDIA_ENDPOINTS",
    "GIT_SHORT_SHA",
    "GOOGLE_GTM_ID",
    "SENTRY_DSN",
    "OPENREPLAY_PROJECT_KEY",
    "STRIPE_PUBLISHABLE_KEY",
]


##################################################################
# OBP API
##################################################################
OBP_SYNC_ENDPOINT = env(
    "OBP_SYNC_ENDPOINT",
    default="https://www.openbroadcast.org/api/v2/obr-sync/",
)
OBP_SYNC_TOKEN = env(
    "OBP_SYNC_TOKEN",
    default="",
)


##################################################################
# OBR API
##################################################################
OBR_SYNC_ENDPOINT = env(
    "OBR_SYNC_ENDPOINT",
    default="https://www.openbroadcast.ch/api/v2/obr-sync/",
)
OBR_SYNC_TOKEN = env(
    "OBR_SYNC_TOKEN",
    default="",
)


##################################################################
# 3rd party services
##################################################################
USERSNAP_API_KEY = env(
    "USERSNAP_API_KEY",
    default=None,
)
SENDGRID_API_KEY = env(
    "SENDGRID_API_KEY",
    default=None,
)


##################################################################
# "CMS"
##################################################################
CMS_PAGES_DIR = env(
    "CMS_PAGES_DIR",
    default=str(PROJECT_ROOT / "content" / "pages"),
)


##################################################################
# Address / Countries
##################################################################
COUNTRIES_FIRST = [
    "CH",
    "FR",
    "DE",
    "IT",
    "AT",
]
COUNTRIES_FIRST_SORT = False
# COUNTRIES_FIRST_BREAK = "--"


##################################################################
# Slack
##################################################################
SLACK_RATING_WEBHOOK = env(
    "SLACK_RATING_WEBHOOK",
    default="",
)


##################################################################
# error reporting & co
##################################################################
SENTRY_DSN = env(
    "SENTRY_DSN",
    default=None,
)

OPENREPLAY_PROJECT_KEY = env(
    "OPENREPLAY_PROJECT_KEY",
    default=None,
)


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
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
