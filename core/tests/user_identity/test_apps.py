from django.apps import apps

from user_identity.apps import UserIdentConfig


def test_apps():

    app_config = UserIdentConfig

    assert app_config.name == "user_identity"
    assert apps.get_app_config("user_identity").name, "user_identity"
