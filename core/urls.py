# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve

SITE_URL = getattr(settings, "SITE_URL")

admin.autodiscover()
admin.site.site_header = "OBR - {}".format(SITE_URL)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("", include("spa.urls")),
]

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
