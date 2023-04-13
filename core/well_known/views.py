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
                            "NOT /admin/*",
                            "NOT /app-bridge/social-auth-redirect/",
                            "NOT /app-bridge/social-auth-redirect/*",
                            "*",
                        ],
                    },
                ],
            },
        },
    )
