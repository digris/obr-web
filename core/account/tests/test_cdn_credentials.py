import datetime
from account.cdn_credentials.cookie import get_signed_cookie, get_cdn_policy


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
