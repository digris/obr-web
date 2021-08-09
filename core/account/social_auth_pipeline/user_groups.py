import logging

from django.conf import settings

WHITELISTED_DOMAINS = getattr(settings, "SOCIAL_AUTH_WHITELISTED_DOMAINS", [])

log = logging.getLogger(__name__)


# pylint: disable=unused-argument,keyword-arg-before-vararg
def add_user_to_team(strategy, user=None, *args, **kwargs):
    """
    assign user to team group.
    also sets staff & email verification flags
    """

    if not (user and user.email):
        return None

    if (
        WHITELISTED_DOMAINS
        and user.email.split("@")[-1].strip() not in WHITELISTED_DOMAINS
    ):
        log.warning(
            "authentication denied. {} not in allowed domains".format(user.email)
        )
        return None

    changed = False

    if WHITELISTED_DOMAINS and not user.is_staff:
        log.info("adding {} to staff".format(user))
        setattr(user, "is_staff", True)
        changed = True

    if changed:
        strategy.storage.user.changed(user)

    return None
