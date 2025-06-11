import os
import sys
from datetime import timedelta
from pathlib import Path
from django.urls import reverse_lazy

import environ

from .. import __version__

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
APP_ROOT = os.path.join(PROJECT_ROOT, "obr_core")

sys.path.insert(0, APP_ROOT)

env = environ.Env(
    DEBUG=(bool, False),
    SITE_URL=(str, "https://openbroadcast.ch"),
    OBP_SYNC_SKIP_MEDIA=(bool, False),
    OBP_SYNC_SKIP_IMAGES=(bool, False),
    # JWT
    JWT_TOKEN_LIFETIME=(int, 60 * 60 * 24 * 28),  # 28 days
    JWT_TOKEN_REFRESH_LIFETIME=(int, 60 * 60 * 24 * 120),  # 120 days
    CDN_POLICY_LIFETIME=(int, 60 * 60 * 24),  # 1 day
    CDN_POLICY_DOMAIN=(str, "openbroadcast.ch"),
)

DEBUG = env("DEBUG")
SECRET_KEY = env(
    "SECRET_KEY",
    default="---secret-key---",
)
SITE_URL = env("SITE_URL").strip("/")

ALLOWED_HOSTS = ["*"]
SESSION_COOKIE_NAME = "sid"
SESSION_COOKIE_SAMESITE = None


INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
    "storages",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_filters",
    "social_django",
    "django_countries",
    "adminsortable2",
    "common",
    "tagging",
    "api_extra",
    "sync",
    "account",
    "app_bridge",
    "user_identity",
    "subscription",
    "donation",
    "identifier",
    "rating",
    "broadcast",
    "catalog",
    "cms",
    "faq",
    "share",
    "redirect",
    "qr_redirect",
    "electronic_mail",
    "stats",
    "newsletter",
    "streaming_services",
    "survey",
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

ROOT_URLCONF = "config.urls"

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
                "django.template.context_processors.i18n",
                "django.contrib.messages.context_processors.messages",
                "django_settings_export.settings_export",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "common.context_processors.version",
                "geolocation.context_processors.geolocation",
                "client_mode.context_processors.client_mode",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


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
    "account.social_auth_pipeline.user_streaming_services.sync_streaming_services",
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

# use unique google account ids instead of email
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# https://developer.spotify.com/documentation/general/guides/scopes/
SOCIAL_AUTH_SPOTIFY_SCOPE = [
    "user-read-private",
    "user-read-email",
    "user-top-read",
    #
    "user-library-read",
    "playlist-modify-private",
]

# spotify oauth2
SOCIAL_AUTH_SPOTIFY_KEY = env(
    "SOCIAL_AUTH_SPOTIFY_KEY",
    default="",
)

SOCIAL_AUTH_SPOTIFY_SECRET = env(
    "SOCIAL_AUTH_SPOTIFY_SECRET",
    default="",
)

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
    "delete_library",
    "listening_history",
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


# additional authentication services (iOS)
GOOGLE_AUTH_CLIENT_ID = env(
    "GOOGLE_AUTH_CLIENT_ID",
    default="",
)
# additional authentication services (one-tap)
GOOGLE_ACCOUNTS_CLIENT_ID = env(
    "GOOGLE_ACCOUNTS_CLIENT_ID",
    default="",
)


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
# USE_L10N = False  # depreciated - check for side effects
USE_TZ = True

DATETIME_FORMAT = "Y-m-d H:i:sO"
DATE_FORMAT = "Y-m-d"


##################################################################
# static files / storage
##################################################################
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

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

GS_MEDIA_BUCKET = env(
    "GS_MEDIA_BUCKET",
    default="obr-media",
)

GS_MASTER_BUCKET = env(
    "GS_MASTER_BUCKET",
    default="obr-master",
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
        # "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
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
        "rating.vote": "1200/minute",  # NOTE: implement separate limit for POST
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # 'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SIMPLE_JWT = {
    "USER_ID_FIELD": "uid",
    "USER_ID_CLAIM": "user_uid",
    # "SLIDING_TOKEN_LIFETIME": timedelta(days=28),
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=120),
    "SLIDING_TOKEN_LIFETIME": timedelta(seconds=env("JWT_TOKEN_LIFETIME")),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(seconds=env("JWT_TOKEN_REFRESH_LIFETIME")),
    # "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.SlidingToken",),
    "AUTH_TOKEN_CLASSES": ("account.jwt_token.tokens.SlidingToken",),
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "account.jwt_token.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "account.jwt_token.serializers.TokenRefreshSlidingSerializer",
}


SPECTACULAR_SETTINGS = {
    "TITLE": "OBR API",
    "DESCRIPTION": "open broadcast - radio",
    "VERSION": str(__version__),
    "SCHEMA_PATH_PREFIX": "/api/v[0-9]",
    "CAMELIZE_NAMES": True,
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_NO_READ_ONLY_REQUIRED": False,
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": False,
    # 'PREPROCESSING_HOOKS': [],
    "SORT_OPERATIONS": True,
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        # "api_extra.drf_spectacular_postprocessors.read_only_response_fields_not_optional",
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
    "SERVERS": [
        {
            "url": "https://openbroadcast.ch",
        },
        {
            "url": "http://local.obr-next:8080",
        },
    ],
    "EXTERNAL_DOCS": {
        "url": "https://github.com/digris/obr-web",
    },
    # "REDOC_UI_SETTINGS": {},  # see template: drf_spectacular/redoc.html
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
        "VoteScopeEnum": "rating.models.VoteScope.choices",
        "VoteSourceEnum": "rating.models.VoteSource.choices",
    },
}


##################################################################
# services
##################################################################
API_BASE_URL = "/api/v1/"

STREAM_LATENCY = 0  # in seconds

STREAM_ENDPOINTS = {
    "dash": "https://stream-abr.openbroadcast.ch/dash/stream.mpd",
    "hls": "https://stream-abr.openbroadcast.ch/hls/manifest.m3u8",
    "icecast": "https://stream.openbroadcast.ch/256.mp3",
    #
    "news": env(
        "STREAM_ENDPOINT_NEWS",
        default="https://stream-abr.openbroadcast.ch/hls/news/",
    )
}

MEDIA_ENDPOINTS = {
    "dash": "https://media.openbroadcast.ch/encoded/",
    "hls": "https://media.openbroadcast.ch/encoded/",
}

IMAGE_RESIZER_ENDPOINT = env(
    "IMAGE_RESIZER_ENDPOINT",
    default="/images/",
)


##################################################################
# CDN
##################################################################
CDN_POLICY_LIFETIME = env.int("CDN_POLICY_LIFETIME")
CDN_POLICY_DOMAIN = env("CDN_POLICY_DOMAIN")


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
STRIPE_WEBHOOK_SECRET = env(
    "STRIPE_WEBHOOK_SECRET",
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
    "API_BASE_URL",
    "IMAGE_RESIZER_ENDPOINT",
    "STREAM_ENDPOINTS",
    "STREAM_LATENCY",
    "MEDIA_ENDPOINTS",
    "GIT_SHORT_SHA",
    "GOOGLE_GTM_ID",
    "GOOGLE_ACCOUNTS_CLIENT_ID",
    "SENTRY_DSN",
    "OPENREPLAY_PROJECT_KEY",
    "STRIPE_PUBLISHABLE_KEY",
    "SSE_PUBLISHER_URL",
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
# STATS ES /API
##################################################################
STATS_ES_API_URL = env(
    "STATS_ES_API_URL",
    default="http://localhost:9200",
)
STATS_ES_API_KEY = env(
    "STATS_ES_API_KEY",
    default="",
)


##################################################################
# SSE Publisher
##################################################################
SSE_PUBLISHER_URL = env(
    "SSE_PUBLISHER_URL",
    default="https://openbroadcast.ch/sse/",
)


##################################################################
# streaming services
##################################################################
STREAMING_SERVICES_SPOTIFY_SOCIAL_AUTH_EMAIL = env(
    "STREAMING_SERVICES_SPOTIFY_SOCIAL_AUTH_EMAIL",
    default="jonas.ohrstrom@digris.ch",
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
MAILCHIMP_API_KEY = env(
    "MAILCHIMP_API_KEY",
    default=None,
)
MAILCHIMP_LIST_ID = env(
    "MAILCHIMP_LIST_ID",
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
# unfold admin
##################################################################
UNFOLD = {
    "SITE_TITLE": "open broadcast - radio",
    "SITE_HEADER": "open broadcast - radio",
    "SITE_SUBHEADER": "eclectic music",
    "SITE_URL": "/",
    "SITE_SYMBOL": "radio",
    "SHOW_HISTORY": False,
    "THEME": "light",
    # "ENVIRONMENT": "config.environment_callback",
    "LOGIN": {
        "redirect_after": lambda request: reverse_lazy(
            "admin:catalog_release_changelist"
        ),
    },
    "BORDER_RADIUS": "3px",
    "COLORS": {
        "base": {
            "50": "249 250 251",
            "100": "243 244 246",
            "200": "229 231 235",
            "300": "209 213 219",
            "400": "156 163 175",
            "500": "107 114 128",
            "600": "75 85 99",
            "700": "55 65 81",
            "800": "31 41 55",
            "900": "17 24 39",
            "950": "3 7 18",
        },
        "primary": {
            "50": "233 237 255",
            "100": "217 221 255",
            "200": "190 198 255",
            "300": "147 153 254",
            "400": "92 101 252",
            "500": "67 76 247",
            "600": "47 51 234",
            "700": "39 42 206",
            "800": "33 37 168",
            "900": "28 31 135",
            "950": "16 17 100"
        },
        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "de": "🇩🇪",
            },
        },
    },
    "SITE_DROPDOWN": [
        {
            "icon": "admin_panel_settings",
            "title": "Admin",
            "link": reverse_lazy("admin:index"),
        },
        {
            "icon": "radio",
            "title": "openbroadcast.ch",
            "link": "https://openbroadcast.ch/",
        },
        {
            "icon": "code",
            "title": "Github",
            "link": "https://github.com/digris/obr-web/",
        },
        {
            "icon": "stacked_line_chart",
            "title": "Analytics",
            "link": "https://analytics.google.com/analytics/web/#/p299020254/reports/intelligenthome",
        },
        {
            "icon": "area_chart",
            "title": "Stats",
            "link": "https://stats.openbroadcast.ch/",
        },
        {
            "icon": "monitoring",
            "title": "Kibana Dashboard",
            "link": "https://openbroadcast.ch/kibana/",
        },
    ],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Catalog",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Tracks",
                        "icon": "library_music",
                        "link": reverse_lazy("admin:catalog_media_changelist"),
                    },
                    # {
                    #     "title": "Masters",
                    #     "icon": "group",
                    #     "link": reverse_lazy("admin:catalog_master_changelist"),
                    # },
                    {
                        "title": "Artists",
                        "icon": "artist",
                        "link": reverse_lazy("admin:catalog_artist_changelist"),
                    },
                    {
                        "title": "Releases",
                        "icon": "album",
                        "link": reverse_lazy("admin:catalog_release_changelist"),
                    },
                    {
                        "title": "Labels",
                        "icon": "apartment",
                        "link": reverse_lazy("admin:catalog_label_changelist"),
                    },
                    {
                        "title": "Moods",
                        "icon": "mood",
                        "link": reverse_lazy("admin:catalog_mood_changelist"),
                    },
                    {
                        "title": "Series",
                        "icon": "sunny",
                        "link": reverse_lazy("admin:catalog_series_changelist"),
                    },
                    {
                        "title": "Playlists",
                        "icon": "playlist_play",
                        "link": reverse_lazy("admin:catalog_playlist_changelist"),
                    },
                ],
            },
            {
                "title": "Broadcast",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Editors",
                        "icon": "group",
                        "link": reverse_lazy("admin:broadcast_editor_changelist"),
                    },
                    {
                        "title": "Emissions",
                        "icon": "event",
                        "link": reverse_lazy("admin:broadcast_emission_changelist"),
                    },
                    {
                        "title": "Emissions (Archived)",
                        "icon": "event",
                        "link": reverse_lazy("admin:stats_emission_changelist"),
                    },
                    {
                        "title": "Airplays",
                        "icon": "event_list",
                        "link": reverse_lazy("admin:catalog_airplay_changelist"),
                    },
                    {
                        "title": "Airplays (Archived)",
                        "icon": "event_list",
                        "link": reverse_lazy("admin:stats_airplay_changelist"),
                    },
                ],
            },
            {
                "title": "Rating",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Votes",
                        "icon": "voting_chip",
                        "link": reverse_lazy("admin:rating_vote_changelist"),
                    },
                ],
            },
            {
                "title": "Subscription",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Subscriptions",
                        "icon": "card_membership",
                        "link": reverse_lazy("admin:subscription_subscription_changelist"),
                    },
                    {
                        "title": "Payments",
                        "icon": "credit_card",
                        "link": reverse_lazy("admin:subscription_payment_changelist"),
                    },
                    {
                        "title": "Vouchers",
                        "icon": "loyalty",
                        "link": reverse_lazy("admin:subscription_voucher_changelist"),
                    },
                    {
                        "title": "Redemptions",
                        "icon": "redeem",
                        "link": reverse_lazy("admin:subscription_redemption_changelist"),
                    },
                ],
            },
            {
                "title": "Donation",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Donations",
                        "icon": "paid",
                        "link": reverse_lazy("admin:donation_donation_changelist"),
                    }
                ],
            },
            {
                "title": "Tagging",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Tags",
                        "icon": "tag",
                        "link": reverse_lazy("admin:tagging_tag_changelist"),
                    },
                ],
            },
            {
                "title": "CMS",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Pages",
                        "icon": "web",
                        "link": reverse_lazy("admin:cms_page_changelist"),
                    },
                ],
            },
            {
                "title": "FAQ",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": reverse_lazy("admin:faq_category_changelist"),
                    },
                    {
                        "title": "Topics",
                        "icon": "quiz",
                        "link": reverse_lazy("admin:faq_topic_changelist"),
                    },
                ],
            },
            {
                "title": "Newsletter",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Newsletters",
                        "icon": "newspaper",
                        "link": reverse_lazy("admin:newsletter_newsletter_changelist"),
                    },
                    {
                        "title": "Subscriptions",
                        "icon": "subscriptions",
                        "link": reverse_lazy("admin:newsletter_subscription_changelist"),
                    },
                ],
            },
            {
                "title": "Stats",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Heartbeat",
                        "icon": "cardiology",
                        "link": reverse_lazy("admin:stats_heartbeat_changelist"),
                    },
                    {
                        "title": "Player Events",
                        "icon": "play_circle",
                        "link": reverse_lazy("admin:stats_playerevent_changelist"),
                    },
                    {
                        "title": "Stream Events",
                        "icon": "stream",
                        "link": reverse_lazy("admin:stats_streamevent_changelist"),
                    },
                ],
            },
            {
                "title": "Admin",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Users",
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:account_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Addresses",
                        "icon": "home",
                        "link": reverse_lazy("admin:account_address_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Groups",
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Auth Tokens",
                        "icon": "token",
                        "link": reverse_lazy("admin:authtoken_tokenproxy_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
}


##################################################################
# logging
##################################################################
LOGGING = {
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
    },
}
