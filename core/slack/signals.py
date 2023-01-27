import logging

from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from rating.models import Vote

from . import bot

SITE_URL = getattr(settings, "SITE_URL", "")

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Vote)
# pylint: disable=unused-argument
def rating_post_save(sender, instance, **kwargs):

    values = {-1: "-", 1: "+"}

    tpl = """*{value}* \tfor <{url}|{name}>
    \tby {user}
    """

    url = f"{SITE_URL}{instance.content_object.get_absolute_url()}"

    md = tpl.format(
        value=values.get(instance.value, instance.value),
        url=url,
        name=str(instance.content_object),
        user=str(instance.user) if instance.user else "anonymous",
    )

    if instance.value < 0:
        md += "\treason: {scope}".format(
            scope=instance.get_scope_display(),
        )

    if instance.comment:
        md += "  \n\t\t_{comment}_".format(
            comment=instance.comment,
        )

    body = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": md,
        },
    }

    if image := instance.content_object.image:
        image_url = f"{SITE_URL}/images/crop/200x200/{image.path}"
        body.update(
            {
                "accessory": {
                    "type": "image",
                    "image_url": image_url,
                    "alt_text": "Image",
                }
            }
        )

    payload = {
        "blocks": [
            body,
        ],
    }

    bot.post(payload=payload, channel="rating")


@receiver(pre_delete, sender=Vote)
# pylint: disable=unused-argument
def rating_pre_delete(sender, instance, **kwargs):

    tpl = """*x* \tfor <{url}|{name}>
    \tby {user}
    """

    url = f"{SITE_URL}{instance.content_object.get_absolute_url()}"

    md = tpl.format(
        url=url,
        name=str(instance.content_object),
        user=str(instance.user) if instance.user else "anonymous",
    )

    body = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": md,
        },
    }

    payload = {
        "blocks": [
            body,
        ],
    }

    bot.post(payload=payload, channel="rating")
