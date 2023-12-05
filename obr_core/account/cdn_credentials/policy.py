import base64
import datetime
import hashlib
import hmac

COOKIE_NAME = "Cloud-CDN-Cookie"
URL_PREFIX = "https://media.openbroadcast.ch/encoded"
KEY_NAME = "cdn-key"
KEY_BASE64 = "uH2LcPhs5zzOLQsu65rtZw=="


def get_signed_cookie(url_prefix, key_name, base64_key, expiration_time):
    encoded_url_prefix = base64.urlsafe_b64encode(
        url_prefix.strip().encode("utf-8"),
    ).decode("utf-8")
    epoch = datetime.datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    policy_pattern = (
        "URLPrefix={encoded_url_prefix}:Expires={expires}:KeyName={key_name}"
    )
    policy = policy_pattern.format(
        encoded_url_prefix=encoded_url_prefix,
        expires=expiration_timestamp,
        key_name=key_name,
    )

    digest = hmac.new(decoded_key, policy.encode("utf-8"), hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(digest).decode("utf-8")

    signed_policy = f"{policy}:Signature={signature}"
    return signed_policy


def get_cdn_policy(seconds_valid=60 * 60):
    signed_policy = get_signed_cookie(
        url_prefix=URL_PREFIX,
        key_name=KEY_NAME,
        base64_key=KEY_BASE64,
        expiration_time=datetime.datetime.now() + datetime.timedelta(seconds_valid),
    )

    return signed_policy
