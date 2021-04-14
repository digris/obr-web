# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import include, path

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse


from drf_yasg.views import get_schema_view
from drf_yasg import openapi


app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="OBR API CORE",
        default_version="v1",
        description="open broadcast radio API",
        terms_of_service="/legal/toc/",
        contact=openapi.Contact(email="info@openbroadcast.ch"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response(
        {
            "schema/": reverse("api:openapi-schema", request=request, format=format),
            "docs/": reverse("api:api-docs", request=request, format=format),
        }
    )


urlpatterns = [
    path("", api_root, name="base"),
    path(
        "schema/",
        schema_view.without_ui(cache_timeout=0),
        name="openapi-schema",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(r"^docs/$", schema_view.with_ui("redoc", cache_timeout=0), name="api-docs"),
    path("account/", include("account.api.urls", "account")),
    path("catalog/", include("catalog.api.urls", "catalog")),
]
