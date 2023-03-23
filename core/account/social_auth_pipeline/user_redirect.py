# pylint: disable=unused-argument,keyword-arg-before-vararg
def registration_redirect(strategy, user=None, request=None, is_new=False, *args, **kwargs):
    # redirect new users to account page
    if is_new:
        strategy.session_set("next", "/account/")
