import logging

from django.conf import settings

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

API_KEY = settings.MAILCHIMP_API_KEY
LIST_ID = settings.MAILCHIMP_LIST_ID

logger = logging.getLogger(__name__)


def get_client(api_key):
    mailchimp_client = MailchimpMarketing.Client()
    try:
        server_prefix = api_key.split("-")[1]
    except (AttributeError, IndexError):
        server_prefix = ""
    mailchimp_client.set_config(
        {
            "api_key": api_key,
            "server": server_prefix,
        },
    )
    return mailchimp_client


client = get_client(API_KEY)


def get_list_info(list_id):
    try:
        return client.lists.get_list(list_id)
    except ApiClientError as error:
        print("error.text", error.text)
        print("error.__dict__", error.__dict__)
        logger.warning("api client error")
        return None


def add_list_member(email, first_name, last_name, language="de"):
    payload = {
        "email_address": email,
        "status": "subscribed",
        "language": language,
        "merge_fields": {
            "FNAME": first_name,
            "LNAME": last_name,
        },
    }

    try:
        return client.lists.add_list_member(
            LIST_ID,
            payload,
        )
    except ApiClientError as error:
        print("ERROR add_list_member")
        print("error.text", error.text)
        print("error.__dict__", error.__dict__)
        logger.warning("api client error")
        return None


def delete_list_member(subscriber_hash):
    try:
        return client.lists.delete_list_member(
            LIST_ID,
            subscriber_hash,
        )
    except ApiClientError as error:
        print("error.text", error.text)
        print("error.__dict__", error.__dict__)
        logger.warning("api client error")
        return None


def get_list_member_tags(subscriber_hash):
    try:
        return client.lists.get_list_member_tags(
            LIST_ID,
            subscriber_hash,
        )
    except ApiClientError as error:
        print("error.text", error.text)
        print("error.__dict__", error.__dict__)
        logger.info("api client error")
        return None


def set_list_member_tag(subscriber_hash, tag, active=True):
    payload = {
        "tags": [
            {
                "name": tag,
                "status": "active" if active else "inactive",
            },
        ],
    }
    try:
        return client.lists.update_list_member_tags(
            LIST_ID,
            subscriber_hash,
            payload,
        )
    except ApiClientError as error:
        print("error.text", error.text)
        print("error.__dict__", error.__dict__)
        logger.info("api client error")
        return None


def subscribe(subscription):
    member_tags = get_list_member_tags(subscription.mailchimp_subscriber_hash)

    print(member_tags)

    if not member_tags:
        add_list_member(
            email=subscription.user.email,
            first_name=subscription.user.first_name,
            last_name=subscription.user.last_name,
        )

    set_list_member_tag(
        subscriber_hash=subscription.mailchimp_subscriber_hash,
        tag=subscription.newsletter.mailchimp_tag,
        active=True,
    )


def unsubscribe(subscription):
    member_tags = get_list_member_tags(subscription.mailchimp_subscriber_hash)

    if not member_tags:
        return

    set_list_member_tag(
        subscriber_hash=subscription.mailchimp_subscriber_hash,
        tag=subscription.newsletter.mailchimp_tag,
        active=False,
    )
