APP_HEADER = "X-Client-App"
APP_DEFAULT = "web"


class ClientModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.client_mode_app = request.headers.get(APP_HEADER, APP_DEFAULT)

        return self.get_response(request)
