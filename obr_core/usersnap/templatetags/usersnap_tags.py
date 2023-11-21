from django import template
from django.conf import settings

API_KEY = settings.USERSNAP_API_KEY


register = template.Library()


@register.inclusion_tag(
    "usersnap/usersnap.html",
    takes_context=True,
)
def usersnap(context):
    try:
        request = context["request"]  # NOQA
    except KeyError:
        return {}

    if request.client_mode == "app":
        return {}

    context.update(
        {
            "api_key": API_KEY,
        },
    )

    if request.user and request.user.is_authenticated:
        context.update(
            {
                "email": request.user.email,
                "uid": request.user.uid,
            },
        )

    return context
