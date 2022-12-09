from django.http import JsonResponse

IOS_APP_ID = "236JDQVAKF.ch.digris.obrapp"


def apple_app_site_association(request):
    """
    see:
    https://developer.apple.com/documentation/xcode/supporting-associated-domains
    """
    return JsonResponse(
        {
            "applinks": {
                "apps": [],
                "details": [
                    {
                        "appID": IOS_APP_ID,
                        "paths": [
                            "NOT /social/*",
                            "NOT /app-bridge/social-auth-redirect/",
                            "NOT /app-bridge/social-auth-redirect/*",
                            "*",
                        ],
                        # "components": [
                        #     {
                        #         "/": "/social/*",
                        #         "exclude": True,
                        #         "comment": "OAuth login flow must be started in the os browser",
                        #     },
                        #     {
                        #         "/": "/app-bridge/social-auth-redirect/*",
                        #         "exclude": True,
                        #         "comment": "Auth redirect to be completed in the os browser",
                        #     },
                        #     {
                        #         "/": "/*",
                        #         "comment": "Matches any URL with a path that starts with /.",
                        #     },
                        # ],
                    }
                ],
            }
        }
    )
