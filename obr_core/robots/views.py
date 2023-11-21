from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: PetalBot",
        "Disallow: /",
        "User-Agent: *",
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
