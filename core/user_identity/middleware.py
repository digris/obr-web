import logging

from .utils import get_user_identity, get_device_key

logger = logging.getLogger(__name__)


class UserIdentityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_identity = get_user_identity(request)
        request.device_key = get_device_key(request)
        response = self.get_response(request)
        response["X-User-Identity"] = request.user_identity
        response["X-Device-Key"] = request.device_key
        return response
