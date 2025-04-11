from django.utils.cache import patch_response_headers


def sitemap_cache_control_view(view_func):
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        # allow CDN to cache for 24h
        response["Cache-Control"] = "public, max-age=86400, s-maxage=86400"
        patch_response_headers(response, cache_timeout=86400)
        return response

    return _wrapped_view
