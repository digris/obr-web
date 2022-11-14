DEFAULT_MODE = "web"


def get_client_mode(request):
    """
    requests made by webview component from iOS app have a user-agent string in the form of: OBR-App-iOS/6
    """
    if user_agent := request.META.get("HTTP_USER_AGENT"):
        return "app" if user_agent.lower().startswith("obr-app-ios") else DEFAULT_MODE
    return DEFAULT_MODE


class ClientModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.client_mode = get_client_mode(request=request)

        return self.get_response(request)
