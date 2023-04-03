import os

import django
from django.core.handlers.asgi import (
    ASGIHandler,
    FileResponse,
    RequestAborted,
    set_script_prefix,
    signals,
    sync_to_async,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.default")


class PatchedASGIHandler(ASGIHandler):
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return
        try:
            body_file = await self.read_body(receive)
        except RequestAborted:
            return
        set_script_prefix(self.get_script_prefix(scope))
        await sync_to_async(signals.request_started.send, thread_sensitive=True)(
            sender=self.__class__,
            scope=scope,
        )
        request, error_response = self.create_request(scope, body_file)
        if request is None:
            await self.send_response(error_response, send)
            return
        response = await self.get_response_async(request)
        response._handler_class = self.__class__
        if isinstance(response, FileResponse):
            response.block_size = self.chunk_size
        await self.send_response(response, send)


def get_asgi_application():
    django.setup(set_prefix=False)
    return PatchedASGIHandler()


application = get_asgi_application()
