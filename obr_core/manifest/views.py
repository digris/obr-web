from django.http import JsonResponse
from django.templatetags.static import static


def manifest_view(request):
    return JsonResponse(
        {
            "name": "open broadcast radio",
            "short_name": "open broadcast",
            "start_url": "/",
            "scope": "/",
            "display": "fullscreen",
            "theme_color": "#000",
            "background_color": "#000",
            "description": "open broadcast hybrid radio",
            "categories": ["music", "radio"],
            "orientation": "portrait",
            "icons": [
                {
                    "src": request.build_absolute_uri(
                        static("assets/manifest/icon-192x192.png")
                    ),
                    "sizes": "192x192",
                    "type": "image/png",
                },
                {
                    "src": request.build_absolute_uri(
                        static("assets/manifest/icon-512x512.png")
                    ),
                    "sizes": "512x512",
                    "type": "image/png",
                },
            ],
            "shortcuts": [
                {
                    "name": "Discover",
                    "short_name": "Discover",
                    "description": "Discover music",
                    "url": "/discover/moods/",
                },
                {
                    "name": "Program",
                    "short_name": "Program",
                    "description": "Program",
                    "url": "/program/",
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
