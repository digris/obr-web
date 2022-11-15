# pylint: disable=unused-argument,keyword-arg-before-vararg
def app_redirect(backend, strategy, *args, **kwargs):

    if strategy.session_get('source') == "app":
        strategy.session_set("next", "/proto/app-bridge/")
