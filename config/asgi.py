import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.default")

django_app = get_asgi_application()

class LifespanShim:

    # Trying to get rid of:
    #     ValueError
    #         Events (total)
    #         Users (90d)
    #         Level: Error
    #         Django can only handle ASGI/HTTP connections, not lifespan.

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "lifespan":
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        else:
            await self.app(scope, receive, send)

application = LifespanShim(django_app)
