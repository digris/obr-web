import logging
from .cookie import get_cdn_policy

CLOUD_CDN_DOMAIN = "next.openbroadcast.ch"
CLOUD_CDN_COOKIE_NAME = "Cloud-CDN-Cookie"

logger = logging.getLogger(__name__)


def set_credentials(response, seconds_valid=60 * 60):
    logger.debug(f"set credentials - valid for: {seconds_valid}")
    policy = get_cdn_policy(seconds_valid=seconds_valid)
    logger.debug(f"policy: {policy}")

    # v1 - "raw"
    cookie_str = f"{CLOUD_CDN_COOKIE_NAME}={policy}; Path=/; Domain={CLOUD_CDN_DOMAIN}; HttpOnly: SameSite=Lax"
    response["Set-Cookie"] = cookie_str

    # v2 - "django"
    # NOTE: this does not work - as django places quotes `"` around the value.
    # response.set_cookie(
    #     key=CLOUD_CDN_COOKIE_NAME,
    #     value=policy,
    #     path="/",
    #     domain=CLOUD_CDN_DOMAIN,
    #     httponly=True,
    #     samesite="Lax",
    # )

    return response


def remove_credentials(response):
    logger.debug("remove credentials")
    response.delete_cookie(
        key=CLOUD_CDN_COOKIE_NAME,
        path="/",
        domain=CLOUD_CDN_DOMAIN,
    )
    return response
