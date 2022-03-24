from .version import get_version, get_short_sha


def version(request):
    ctx = {
        "version": get_version(),
        "version_sha": get_short_sha(),
    }
    return ctx
