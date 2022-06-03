import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from rating.models import Vote

from . import bot

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Vote)
# pylint: disable=unused-argument
def rating_post_save(sender, instance, created, **kwargs):

    icons = {
        -1: "⚡",
        1: "♥",
    }

    md = f"{icons.get(instance.value, instance.value)} by {instance.user or 'anonymous'} for <fakeLink.toEmployeeProfile.org|{instance.content_object}>"

    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": md,
                },
                "accessory": {
                    "type": "image",
                    "image_url": "http://placekitten.com/700/500",
                    "alt_text": "Multiple cute kittens",
                },
            },
        ],
    }

    bot.post(payload=payload, channel="rating")
