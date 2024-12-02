from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from spa.views import SPA404View, SPAIndexView


admin.autodiscover()
admin.site.site_header = "open broadcast radio"

urlpatterns = i18n_patterns(
    re_path(r"^api/v1/", include("config.urls_api", namespace="api")),
    prefix_default_language=False,
)

urlpatterns += [
    # metadata
    path("", include("robots.urls", namespace="robots")),
    path("", include("manifest.urls", namespace="manifest")),
    path(".well-known/", include("well_known.urls", namespace="well-known")),
    path("admin/", admin.site.urls),
    path("social/", include("social_django.urls", namespace="social")),
    path("app-bridge/", include("app_bridge.urls", namespace="app-bridge")),
    path(
        "code/",
        include("subscription.urls_voucher", namespace="subscription-voucher"),
    ),
    path(
        "qr/",
        include("qr_redirect.urls", namespace="qr-redirect"),
    ),
    path(
        "stream/",
        include("redirect.urls_stream", namespace="redirect-stream"),
    ),
    # avoid serving SPA view for admin & API
    re_path(r"^api/v1/", SPA404View.as_view()),
    re_path(r"^admin/", SPA404View.as_view()),
    re_path(r"^static/", SPA404View.as_view()),
    # use SPA view for other routes
    path("", SPAIndexView.as_view()),
    re_path(r"^(?P<path>.*)/$", SPAIndexView.as_view()),
]

if settings.DEBUG:
    # NOTE: media serving only works with local storage
    urlpatterns = [
        # media - encoded
        re_path(
            r"^encoded/(?P<path>.*)$",
            serve,
            {
                "document_root": "data/encoded/",
                "show_indexes": True,
            },
        ),
        # media - masters
        re_path(
            r"^master/(?P<path>.*)$",
            serve,
            {
                "document_root": "data/master/",
                "show_indexes": True,
            },
        ),
    ] + urlpatterns
    if "dev" in settings.INSTALLED_APPS:
        urlpatterns = [
            path("dev/", include("dev.urls", namespace="dev")),
        ] + urlpatterns

if not settings.DEBUG:
    urlpatterns = [
        re_path(
            r"^static/(?P<path>.*)$",
            serve,
            {
                "document_root": settings.STATIC_ROOT,
            },
        ),
    ] + urlpatterns
