from django.templatetags.static import static
from django.http import JsonResponse


def manifest_view(request):
    return JsonResponse(
        {
            "name": "open broadcast radio",
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
                    "url": "/discover/moods/",
                },
                {
                    "name": "Program",
                    "short_name": "Program",
                    "description": "Program",
                    "url": "/program/",
                },
            ],
        }
    )
