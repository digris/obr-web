# pylint: disable=unused-argument,keyword-arg-before-vararg
def app_redirect(backend, strategy, user, *args, **kwargs):
    if user and user.email and strategy.session_get("source") == "app":
        pass
