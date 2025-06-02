from urllib.parse import urlparse

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    # NOTE: disallow all crawlers in case we're not on the primary domain
    site_host = urlparse(settings.SITE_URL).hostname
    request_host = request.get_host().split(":")[0]

    if site_host != request_host:
        lines = [
            "User-Agent: *",
            "Disallow: /",
        ]
    else:
        lines = [
            "User-Agent: PetalBot",
            "Disallow: /",
            "User-Agent: *",
            "Disallow: /program/",
            "Disallow: /collection/",
            "Disallow: /admin/",
            "Allow: /program/$",
        ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
