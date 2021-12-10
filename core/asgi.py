import os
import django
from django.core.handlers.asgi import ASGIHandler, ThreadSensitiveContext


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.default")


class PatchedASGIHandler(ASGIHandler):
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        async with ThreadSensitiveContext():
            await self.handle(scope, receive, send)


def get_asgi_application():
    django.setup(set_prefix=False)
    return PatchedASGIHandler()


application = get_asgi_application()
