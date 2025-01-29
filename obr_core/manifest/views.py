from django.http import JsonResponse
from django.templatetags.static import static


def manifest_view(request):
    return JsonResponse(
        {
            "name": "open broadcast radio",
            "short_name": "open broadcast",
            "id": "/",
            "start_url": "/",
            "scope": "/",
            "display": "standalone",
            "theme_color": "#000000",
            "background_color": "#000000",
            "description": "open broadcast - eclectic music",
            "categories": ["music", "radio"],
            "orientation": "portrait",
            "icons": [
                {
                    "src": request.build_absolute_uri(
                        static("assets/manifest/icon-192x192.png"),
                    ),
                    "sizes": "192x192",
                    "type": "image/png",
                },
                {
                    "src": request.build_absolute_uri(
                        static("assets/manifest/icon-512x512.png"),
                    ),
                    "sizes": "512x512",
                    "type": "image/png",
                },
            ],
            "screenshots": [
                {
                    "src": request.build_absolute_uri(
                        static("assets/manifest/screenshot-412x914.png"),
                    ),
                    "form_factor": "narrow",
                    "sizes": "412x914",
                    "type": "image/png",
                },
                {
                    "src": request.build_absolute_uri(
                        static("assets/manifest/screenshot-1600x960.png"),
                    ),
                    "form_factor": "wide",
                    "sizes": "1600x960",
                    "type": "image/png",
                },
            ],
            "shortcuts": [
                {
                    "name": "Discover",
                    "short_name": "Discover",
                    "description": "Discover music",
                    "url": "/discover/moods/",
                    "icons": [
                        {
                            "src": request.build_absolute_uri(
                                static("assets/manifest/icon-192x192.png"),
                            ),
                            "sizes": "192x192",
                            "type": "image/png",
                        },
                    ],
                },
                {
                    "name": "Shows",
                    "short_name": "Shows",
                    "description": "Shows",
                    "url": "/discover/playlists/",
                    "icons": [
                        {
                            "src": request.build_absolute_uri(
                                static("assets/manifest/icon-192x192.png"),
                            ),
                            "sizes": "192x192",
                            "type": "image/png",
                        },
                    ],
                },
                {
                    "name": "Program",
                    "short_name": "Program",
                    "description": "Program",
                    "url": "/program/",
                    "icons": [
                        {
                            "src": request.build_absolute_uri(
                                static("assets/manifest/icon-192x192.png"),
                            ),
                            "sizes": "192x192",
                            "type": "image/png",
                        },
                    ],
                },
            ],
            "prefer_related_applications": True,
            "related_applications": [
                {
                    "platform": "itunes",
                    "url": "https://itunes.apple.com/app/ch-digris-obrapp/id1643695398",
                },
            ],
        },
    )
