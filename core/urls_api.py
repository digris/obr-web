from django.urls import include, path

# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


app_name = "api"


@api_view(["GET"])
@permission_classes([AllowAny])
# pylint: disable=redefined-builtin
def api_root(request, format=None):
    return Response(
        {
            "schema/": reverse(
                "api:schema",
                request=request,
                format=format,
            ),
            "docs/": reverse(
                "api:redoc",
                request=request,
                format=format,
            ),
            "swagger-docs/": reverse(
                "api:swagger-ui",
                request=request,
                format=format,
            ),
            "version/": reverse(
                "api:version:version",
                request=request,
            ),
        }
    )


urlpatterns = [
    path(
        "",
        api_root,
        name="base",
    ),
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "schema-json/",
        SpectacularJSONAPIView.as_view(),
        name="schema-json",
    ),
    # Optional UI:
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="api:schema"),
        name="redoc",
    ),
    path(
        "version/",
        include("base.api.urls_version", "version"),
    ),
    path(
        "account/",
        include("account.api.urls", "account"),
    ),
    path(
        "subscription/",
        include("subscription.api.urls", "subscription"),
    ),
    path(
        "rating/",
        include("rating.api.urls", "rating"),
    ),
    path(
        "search/",
        include("search.api.urls", "search"),
    ),
    path(
        "catalog/",
        include("catalog.api.urls", "catalog"),
    ),
    path(
        "redirect/",
        include("redirect.api.urls", "redirect"),
    ),
    path(
        "broadcast/",
        include("broadcast.api.urls", "broadcast"),
    ),
    path(
        "stats/",
        include("stats.api.urls", "stats"),
    ),
    path(
        "cms/",
        include("cms.api.urls", "cms"),
    ),
    path(
        "sync/",
        include("sync.api.urls", "sync"),
    ),
    path(
        "pub-sub-bridge/",
        include("pub_sub_bridge.api.urls", "pub_sub_bridge"),
    ),
]
