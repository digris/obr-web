import base64
import datetime
import hashlib
import hmac


def sign_cookie(url_prefix, key_name, base64_key, expiration_time):
    """Gets the Signed cookie value for the specified URL prefix and configuration.

    Args:
        url_prefix: URL prefix to sign as a string.
        key_name: name of the signing key as a string.
        base64_key: signing key as a base64 encoded string.
        expiration_time: expiration time as a UTC datetime object.

    Returns:
        Returns the Cloud-CDN-Cookie value based on the specified configuration.
    """
    encoded_url_prefix = base64.urlsafe_b64encode(
        url_prefix.strip().encode("utf-8")
    ).decode("utf-8")
    epoch = datetime.datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    policy_pattern = (
        u"URLPrefix={encoded_url_prefix}:Expires={expires}:KeyName={key_name}"
    )
    policy = policy_pattern.format(
        encoded_url_prefix=encoded_url_prefix,
        expires=expiration_timestamp,
        key_name=key_name,
    )

    digest = hmac.new(decoded_key, policy.encode("utf-8"), hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(digest).decode("utf-8")

    signed_policy = u"Cloud-CDN-Cookie={policy}:Signature={signature}".format(
        policy=policy, signature=signature
    )
    # print(signed_policy)
    return signed_policy


def get_signed_cookie():
    cookie = sign_cookie(
        url_prefix="https://media.next.openbroadcast.ch/encoded",
        key_name="cdn-key",
        base64_key="uH2LcPhs5zzOLQsu65rtZw==",
        expiration_time=datetime.datetime.now() + datetime.timedelta(seconds=60 * 60),
    )
    return cookie
