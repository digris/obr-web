from datetime import datetime

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

import requests
from common.models.context_managers import suppress_auto_now
from rating.models import Vote, VoteScope, VoteSource

OBR_SYNC_ENDPOINT = getattr(settings, "OBR_SYNC_ENDPOINT", None)
OBR_SYNC_TOKEN = getattr(settings, "OBR_SYNC_TOKEN", None)

CT_MAP = {
    "alibrary.media": "catalog.media",
}


def load_votes():
    url = f"{OBR_SYNC_ENDPOINT}anonymous-ratings/?limit=2000"
    headers = {
        "Authorization": f"Token {OBR_SYNC_TOKEN}",
    }
    ratings = []
    while url:
        r = requests.get(url, headers=headers)
        data = r.json()
        url = data["next"]
        ratings += data["results"]
    return ratings


def create_votes(votes_data):
    votes_to_create = []
    for vote in votes_data:
        value = vote["value"]
        created = vote["created"]
        updated = vote["updated"]
        co_uuid = vote["obj_uuid"]
        session_key = vote["session_key"]
        co_ct = vote["obj_ct"]

        ct = CT_MAP.get(co_ct)
        if not ct:
            continue

        created = datetime.fromisoformat(created)
        # created = timezone.make_aware(created)

        updated = datetime.fromisoformat(updated)
        # updated = timezone.make_aware(updated)

        model_class = apps.get_model(*ct.split("."))

        # print(ct, co_uuid)
        try:
            obj = model_class.objects.get(uuid=co_uuid)
        except model_class.DoesNotExist as e:
            # print(e, co_uuid)
            continue

        content_type = ContentType.objects.get_for_model(obj)

        try:
            # for "uniqueness" we just use timestamps & key. there are just a couple of votes per week ;)
            # so this can be considered safe...
            vote = Vote.objects.get(
                user_identity=f"anonymous:{session_key}",
                updated=updated,
                content_type=content_type,
                object_id=obj.id,
            )
            print("got vote", vote)

        except Vote.DoesNotExist:
            vote = Vote(
                user_identity=f"anonymous:{session_key}",
                source=VoteSource.LIVE,
                scope=VoteScope.UNDEFINED,
                value=value,
                created=created,
                updated=updated,
                content_type=content_type,
                object_id=obj.id,
            )
            votes_to_create.append(vote)
            print("create vote", vote)

    print(len(votes_to_create))

    if votes_to_create:
        with suppress_auto_now(Vote, ["created", "updated"]):
            Vote.objects.bulk_create(votes_to_create)


class Command(BaseCommand):
    help = "Sync anonymous ratings from OBR"

    def handle(self, *args, **options):
        votes_data = load_votes()

        # for vote in votes_data:
        #     print(vote)

        create_votes(votes_data=votes_data)

        self.stdout.write(f"sync completed for {len(votes_data)} ratings")
