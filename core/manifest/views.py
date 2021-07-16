# -*- coding: utf-8 -*-
from django.templatetags.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def manifest_view(request):
    return Response(
        {
            "name": "open broadcast",
            "short_name": "open broadcast",
            "start_url": "/",
            "scope": "/",
            "display": "standalone",
            "theme_color": "#FFF",
            "background_color": "#FFF",
            "description": "open broadcast hybrid radio",
            "icons": [
                {
                    "src": static("assets/manifest/icon-192x192.png"),
                    "sizes": "192x192",
                    "type": "image/png",
                },
                {
                    "src": static("assets/manifest/icon-512x512.png"),
                    "sizes": "512x512",
                    "type": "image/png",
                },
            ],
            "shortcuts": [
                {
                    "name": "Discover",
                    "short_name": "Discover",
                    "description": "Discover music",
                    "url": "/discover",
                },
            ],
        }
    )
