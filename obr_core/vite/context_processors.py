from django.conf import settings

VITE_SERVER_PORT = getattr(settings, "VITE_SERVER_PORT", 3000)


def get_vite_server_url(request):
    hostname = request.get_host().split(":")[0]
    return f"//{hostname}:{VITE_SERVER_PORT}"


def vite_proxied(request):
    if hasattr(request, "vite_proxied"):
        cxt = {
            "vite_proxied": request.vite_proxied,
            "vite_server_url": get_vite_server_url(request),
        }
        return cxt

    return {}
