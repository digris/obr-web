import logging

from django.conf import settings

WHITELISTED_DOMAINS = getattr(settings, "SOCIAL_AUTH_WHITELISTED_DOMAINS")

log = logging.getLogger(__name__)


def add_user_to_team(strategy, details, user=None, *args, **kwargs):
    """
    assign user to team group.
    also sets staff & email verification flags
    """

    group_name = "Team"

    if not (user and user.email):
        return

    if (
        WHITELISTED_DOMAINS
        and user.email.split("@")[-1].strip() not in WHITELISTED_DOMAINS
    ):
        log.warning(
            "authentication denied. {} not in allowed domains".format(user.email)
        )
        return

    changed = False

    # if not user.email_verified:
    #     log.info("set email for {} as verified".format(user))
    #     setattr(user, "email_verified", True)
    #     changed = True

    if not user.is_staff:
        log.info("adding {} to staff".format(user))
        setattr(user, "is_staff", True)
        changed = True

    # if not user.groups.filter(name=group_name).exists():
    #     log.info("adding {} to {}".format(user, group_name))
    #     group_qs = Group.objects.filter(name=group_name)
    #     if group_qs.exists():
    #         group_qs.first().user_set.add(user)
    #         changed = True

    if changed:
        strategy.storage.user.changed(user)
