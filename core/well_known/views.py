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
                        "appIDs": [
                            IOS_APP_ID,
                        ],
                        "components": [
                            {
                                "/": "/*",
                                "comment": "Matches any URL with a path that starts with /.",
                            },
                        ],
                    }
                ],
            }
        }
    )
