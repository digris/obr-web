from django.urls import include, path

from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

app_name = "api"


@extend_schema(
    operation_id="base",
    description="API Root, providing human readable entry points.",
    responses={
        200: inline_serializer(
            name="TOC",
            fields={},
        ),
    },
)
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
                "api:base:version",
                request=request,
            ),
            "settings/": reverse(
                "api:base:settings",
                request=request,
            ),
            "broadcast/": reverse(
                "api:broadcast:api-root",
                request=request,
            ),
            "catalog/": reverse(
                "api:catalog:api-root",
                request=request,
            ),
            "faq/": reverse(
                "api:faq:api-root",
                request=request,
            ),
        },
    )


urlpatterns = [
    path(
        "",
        api_root,
        name="base",
    ),
    path(
        "jwt/",
        TokenObtainSlidingView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        "jwt/refresh/",
        TokenRefreshSlidingView.as_view(),
        name="token-refresh",
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
    # Core API
    path(
        "base/",
        include("base.api.urls", "base"),
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
        "faq/",
        include("faq.api.urls", "faq"),
    ),
    path(
        "redirect/",
        include("redirect.api.urls", "redirect"),
    ),
    path(
        "playout/",
        include("playout.api.urls", "playout"),
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
        "newsletter/",
        include("newsletter.api.urls", "newsletter"),
    ),
    path(
        "sync/",
        include("sync.api.urls", "sync"),
    ),
]
