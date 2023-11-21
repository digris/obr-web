from .version import get_short_sha, get_version


def version(request):
    ctx = {
        "version": get_version(),
        "version_sha": get_short_sha(),
    }
    return ctx
