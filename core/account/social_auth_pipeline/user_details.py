# pylint: disable=unused-argument,keyword-arg-before-vararg
def get_user_details(  # NOQA: C901
    backend,
    strategy,
    details,
    response,
    user=None,
    *args,
    **kwargs,
):
    if not user:
        return

    request = strategy.request
    changed = False

    if backend.name == "google-oauth2":
        if not user.first_name and "given_name" in response:
            user.first_name = response["given_name"]
            changed = True

        if not user.last_name and "family_name" in response:
            user.last_name = response["family_name"]
            changed = True

    if backend.name == "deezer":
        if not user.first_name and "firstname" in response:
            user.first_name = response["firstname"]
            changed = True

        if not user.last_name and "lastname" in response:
            user.last_name = response["lastname"]
            changed = True

    if not user.country and request.geolocation_country:
        user.country = request.geolocation_country
        changed = True

    if changed:
        strategy.storage.user.changed(user)
