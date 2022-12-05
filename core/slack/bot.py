import logging

from django.conf import settings

from slack_sdk.errors import SlackApiError
from slack_sdk.webhook import WebhookClient

logger = logging.getLogger(__name__)

RATING_WEBHOOK = getattr(settings, "SLACK_RATING_WEBHOOK")


CHANNELS = {
    "rating": RATING_WEBHOOK,
}


def post(payload, channel=None):
    url = CHANNELS.get(channel)
    if not url:
        logger.warning(f"webhook url not configured for channel: {channel}")
        return
    client = WebhookClient(url, logger=logger)
    try:
        response = client.send(**payload)
    except SlackApiError as e:
        logger.warning(f"unable to post to slack channel: {e}")
        return

    try:
        assert response.status_code == 200
        assert response.body == "ok"
    except AssertionError as e:
        logger.warning(f"unable to post to slack channel: {response.status_code} {e}")


def post_text(text, channel=None):
    payload = {
        "text": text,
    }
    post(payload, channel)


def post_md(md, channel=None):
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": md,
                },
            },
        ],
    }
    post(payload, channel)
