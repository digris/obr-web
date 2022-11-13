from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve

from spa.views import SPAIndexView, SPA404View

# from manifest.views import manifest

SITE_URL = getattr(settings, "SITE_URL")

admin.autodiscover()
admin.site.site_header = "open broadcast radio"

urlpatterns = i18n_patterns(
    re_path(r"^api/v1/", include("core.urls_api", namespace="api")),
    prefix_default_language=False,
)

urlpatterns += [
    path("", include("manifest.urls", namespace="manifest")),
    path("", include("robots.urls", namespace="robots")),
    # path("api/v1/", include("core.urls_api", namespace="api")),
    path("admin/", admin.site.urls),
    path("social/", include("social_django.urls", namespace="social")),
    path(
        "code/", include("subscription.urls_voucher", namespace="subscription-voucher")
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
    urlpatterns = [
        path(
            "electronic-mail/",
            include("electronic_mail.urls", namespace="electronic_mail"),
        ),
        re_path(
            r"^encoded/(?P<path>.*)$",
            serve,
            {
                "document_root": "data/encoded/",
                "show_indexes": True,
            },
        ),
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
