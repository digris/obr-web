# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from graphene_django.views import GraphQLView

SITE_URL = getattr(settings, "SITE_URL")

admin.autodiscover()
admin.site.site_header = "OBR - {}".format(SITE_URL)

urlpatterns = [
    path("api/v1/", include("core.urls_api", namespace="api")),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    # path("graphql", GraphQLView.as_view(graphiql=True)),
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
