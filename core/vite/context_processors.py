def vite_proxied(request):
    if hasattr(request, "vite_proxied"):
        cxt = {"vite_proxied": request.vite_proxied}
        return cxt

    return {}
