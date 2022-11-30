from django.urls import reverse


# pylint: disable=unused-argument,keyword-arg-before-vararg
def app_redirect(backend, strategy, user, *args, **kwargs):

    if not (user and user.email):
        return None

    if strategy.session_get("source") == "app":
        url = reverse("app_bridge:social-auth-redirect")
        strategy.session_set("next", url)
