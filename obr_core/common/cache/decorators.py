from functools import wraps

from django.views.decorators.cache import cache_page

IGNORE_CACHE_HEADER = "X-No-Cache"


def ignorable_cache_page(timeout):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if IGNORE_CACHE_HEADER in request.headers:
                return view_func(request, *args, **kwargs)
            else:
                return cache_page(timeout)(view_func)(request, *args, **kwargs)

        return _wrapped_view

    return decorator
