# -*- coding: utf-8 -*-
import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from rating.models import Vote
from sync import api_client

logger = logging.getLogger(__name__)

CT_MAP = {
    "alibrary.media": "catalog.media",
    "alibrary.artist": "catalog.artist",
    "alibrary.release": "catalog.release",
    "alibrary.playlist": "catalog.playlist",
    # "alibrary.label": "catalog.label",
    "profiles.profile": "broadcast.editor",
}


def sync_user_votes(user):
    # NOTE: not sure where this should go. could also be implemented in rating module.
    logger.debug(f"{user.ct_uid} sync votes")

    try:
        params = {
            "limit": 10000,
            "email": user.email,
            # "email": "jonas@digris.ch",
        }
        data = api_client.get("votes/", params=params)
    except api_client.APIClientException as e:
        logger.error(f"unable to get user: {user} - {e}")
        return None

    for vote in data.get("results", []):
        try:
            value = vote.get("value")
            co = vote.get("co")
            co_uuid = co.get("uuid")
            co_ct = co.get("ct")
        except (KeyError, AttributeError):
            continue
        # print(vote, co)
        ct = CT_MAP.get(co_ct)
        if not ct:
            print(f"invalid ct: {co_ct}")
            continue

        model_class = apps.get_model(*ct.split("."))
        try:
            obj = model_class.objects.get(uuid=co_uuid)
        except model_class.DoesNotExist:
            continue

        content_type = ContentType.objects.get_for_model(obj)
        try:
            vote = Vote.objects.get(
                user=user,
                content_type=content_type,
                object_id=obj.id,
            )
            if vote.value != value:
                Vote.objects.filter(id=vote.id).update(
                    value=value,
                )
        except Vote.DoesNotExist:
            vote = Vote(
                user=user,
                value=value,
                content_type=content_type,
                object_id=obj.id,
            )
            vote.save()
        # print(f"// {value}", content_object)

    return None


# pylint: disable=unused-argument
def sync_user(user, **kwargs):

    update = {}

    type(user).objects.filter(id=user.id).update(**update)

    sync_user_votes(user=user)

    logger.info(f"sync completed for {user.ct}{user.uid}")

    return user
