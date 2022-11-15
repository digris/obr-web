# pylint: disable=unused-argument,keyword-arg-before-vararg
def get_user_details(backend, strategy, details, response, user=None, *args, **kwargs):

    if not user:
        return

    request = strategy.request
    changed = False

    # # TODO: move to separate pipeline
    # if strategy.session_get('source') == "app":
    #     strategy.session_set("next", "/proto/app-bridge/")

    if backend.name == "google-oauth2":

        if not user.first_name and "given_name" in response:
            user.first_name = response["given_name"]
            changed = True

        if not user.last_name and "family_name" in response:
            user.last_name = response["family_name"]
            changed = True

    if not user.country and request.geolocation_country:
        user.country = request.geolocation_country
        changed = True

    if changed:
        strategy.storage.user.changed(user)
