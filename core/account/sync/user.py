import logging
from datetime import datetime
from django.apps import apps
from django.utils import timezone
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


def sync_user_account(user):
    logger.info(f"{user.ct_uid} sync account")

    if not user.obp_id:
        logger.warning(f"user {user.uid} has no obp id")
        return None

    try:
        data = api_client.get(f"accounts/{user.obp_id}/")
    except api_client.APIClientException as e:
        logger.error(f"unable to get user: {user} - {e}")
        return None

    # pylint: disable=import-outside-toplevel
    from account.models import User, Address, Gender

    update = {}

    if date_joined := data.get("date_joined"):
        try:
            date_joined = timezone.make_aware(datetime.fromisoformat(date_joined))
            if date_joined < user.date_joined:
                update.update(
                    {
                        "date_joined": date_joined,
                    }
                )
        except TypeError:
            pass

    if date_of_birth := data.get("birth_date"):
        update.update(
            {
                "date_of_birth": date_of_birth,
            }
        )

    if phone := data.get("phone_mobile"):
        update.update(
            {
                "phone": phone,
            }
        )

    if gender := data.get("gender"):
        values = {
            "female": Gender.FEMALE,
            "male": Gender.MALE,
            "other": Gender.OTHER,
        }
        update.update(
            {
                "gender": values.get(gender, Gender.UNDEFINED),
            }
        )

    User.objects.filter(id=user.id).update(**update)

    if address := data.get("address"):
        try:
            address_obj = user.address
        except Address.DoesNotExist:
            address_obj = Address(
                user=user,
            )
            address_obj.save()

        Address.objects.filter(id=address_obj.id).update(
            line_1=address.get("line_1") or "",
            line_2=address.get("line_2") or "",
            postal_code=address.get("postal_code") or "",
            city=address.get("city") or "",
            country=address.get("country"),
        )

    user.refresh_from_db()
    return user


def sync_user_votes(user):
    # NOTE: not sure where this should go. could also be implemented in rating module.
    logger.info(f"{user.ct_uid} sync votes")

    try:
        params = {
            "limit": 10000,
            "email": user.email,
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

        ct = CT_MAP.get(co_ct)
        if not ct:
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
        logger.debug(f"synced vote on {obj} for {user}")

    return None


# pylint: disable=unused-argument
def sync_user(user, **kwargs):

    update = {}

    type(user).objects.filter(id=user.id).update(**update)

    sync_user_account(user=user)

    sync_user_votes(user=user)

    logger.info(f"sync completed for {user.ct}{user.uid}")

    return user
