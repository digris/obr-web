import datetime
import pytest
from http.cookies import SimpleCookie
from freezegun import freeze_time

from account.cdn_credentials.cookie import get_signed_cookie, get_cdn_policy
from account.cdn_credentials.utils import set_credentials, remove_credentials


def test_get_signed_cookie():
    url_prefix = "https://signed.example.org/private"
    key_name = "the-key"
    base64_key = "AABBCCDD"
    expiration_time = datetime.datetime(2030, 1, 1)

    signed_policy = get_signed_cookie(url_prefix, key_name, base64_key, expiration_time)

    assert (
        signed_policy
        == "URLPrefix=aHR0cHM6Ly9zaWduZWQuZXhhbXBsZS5vcmcvcHJpdmF0ZQ==:Expires=1893456000:KeyName=the-key:Signature=Fe7bCuIWP2eZc7GCAed5_DlIkQY="
    )


@freeze_time("2012-01-01 00:00:00", tz_offset=0)
def test_get_cdn_policy():
    policy = get_cdn_policy()

    assert (
        policy
        == "URLPrefix=aHR0cHM6Ly9tZWRpYS5uZXh0Lm9wZW5icm9hZGNhc3QuY2gvZW5jb2RlZA==:Expires=1636416000:KeyName=cdn-key:Signature=c4O57_Tajb7N2YWpPCY5vnOF15Y="
    )


@pytest.mark.django_db
def test_set_credentials(client):
    response = client.get("/")
    response = set_credentials(response)

    assert response["Set-Cookie"]


@pytest.mark.django_db
def test_remove_credentials(client):
    response = client.get("/")
    response = remove_credentials(response)
    assert (
        str(response.cookies)
        == 'Set-Cookie: Cloud-CDN-Cookie=""; Domain=next.openbroadcast.ch; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/'
    )
