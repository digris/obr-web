from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


from urllib.request import urlopen


def get_user_details(backend, strategy, details, response, user=None, *args, **kwargs):

    if not user:
        return

    changed = False

    if backend.name == "google-oauth2":

        print(response)

        if not user.first_name and "given_name" in response:
            user.first_name = response["given_name"]
            changed = True

        if not user.last_name and "family_name" in response:
            user.last_name = response["family_name"]
            changed = True

    if changed:
        strategy.storage.user.changed(user)
