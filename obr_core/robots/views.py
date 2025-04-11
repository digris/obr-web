from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: PetalBot",
        "Disallow: /",
        "User-Agent: *",
        "Disallow: /program/",
        "Disallow: /collection/",
        "Disallow: /admin/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
