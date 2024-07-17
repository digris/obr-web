import datetime

import pytest
from account.cdn_credentials.policy import get_cdn_policy, get_signed_cookie
from account.cdn_credentials.utils import remove_credentials, set_credentials
from freezegun import freeze_time


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
        == "URLPrefix=aHR0cHM6Ly9tZWRpYS5vcGVuYnJvYWRjYXN0LmNoL2VuY29kZWQ=:Expires=1325462400:KeyName=cdn-key:Signature=UDa_H9Bz86Vjn5ISTxlgQARYgNI="
    )

    expires = int(policy.split(":")[1].split("=")[1])

    # NOTE: should be valid for 24 hours
    assert datetime.datetime.utcfromtimestamp(expires) == datetime.datetime(2012, 1, 2, 0, 0)


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
        == 'Set-Cookie: Cloud-CDN-Cookie=""; Domain=openbroadcast.ch; expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; Path=/'
    )
