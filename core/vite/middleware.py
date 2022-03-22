# -*- coding: utf-8 -*-
import logging

from django.conf import settings

PROXIED_HEADER = "HTTP_" + getattr(
    settings, "VITE_PROXIED_HEADER", "X-VITE-PROXIED"
).replace("-", "_")

log = logging.getLogger(__name__)


class ViteProxiedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get(PROXIED_HEADER, False):
            request.vite_proxied = True

        response = self.get_response(request)
        return response
