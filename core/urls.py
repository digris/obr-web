# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from spa.views import SPAIndexView, SPA404View

# from manifest.views import manifest

SITE_URL = getattr(settings, "SITE_URL")

admin.autodiscover()
admin.site.site_header = "open broadcast radio"

urlpatterns = [
    path("", include("manifest.urls", namespace="manifest")),
    path("api/v1/", include("core.urls_api", namespace="api")),
    path("admin/", admin.site.urls),
    path("social/", include("social_django.urls", namespace="social")),
    # avoid serving SPA view for admin & API
    re_path(r"^api/v1/", SPA404View.as_view()),
    re_path(r"^admin/", SPA404View.as_view()),
    re_path(r"^static/", SPA404View.as_view()),
    # use SPA view for all other routes
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
