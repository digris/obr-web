DEFAULT_MODE = "web"


def get_client_mode(request):
    """
    requests made by webview component from iOS app have a user-agent string in the form of:
    Mozilla/5.0 (iPhone; CPU iPhone OS like Mac OS X) OBR-App-iOS/1.0.2.6
    """
    if user_agent := request.META.get("HTTP_USER_AGENT"):
        return (
            "app" if "obr-app-ios/" in user_agent.lower().startswith else DEFAULT_MODE
        )
    return DEFAULT_MODE


class ClientModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.client_mode = get_client_mode(request=request)

        return self.get_response(request)
