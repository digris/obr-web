# -*- coding: utf-8 -*-
import logging
from .utils import get_user_identity

logger = logging.getLogger(__name__)


class UserIdentityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if not (request.user.is_authenticated and request.session.session_key):
        #     request.session.create()
        #     request.session["key"] = "123"
        #     logger.debug(f"created anonymous session: {request.session.session_key}")

        request.user_identity = get_user_identity(request)

        response = self.get_response(request)
        response["X-User-Identity"] = request.user_identity
        return response
