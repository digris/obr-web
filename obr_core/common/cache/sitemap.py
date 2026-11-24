from django.utils.cache import patch_response_headers
from django.views.decorators.cache import cache_page

CACHE_TIMEOUT = 60 * 60 * 24


def sitemap_cache_control_view(view_func):
    # building the sitemap is expensive - cache it server-side
    cached_view_func = cache_page(CACHE_TIMEOUT)(view_func)

    def _wrapped_view(request, *args, **kwargs):
        response = cached_view_func(request, *args, **kwargs)
        # allow CDN to cache for 24h
        response["Cache-Control"] = "public, max-age=86400, s-maxage=86400"
        patch_response_headers(response, cache_timeout=CACHE_TIMEOUT)
        return response

    return _wrapped_view
