import logging
import bleach

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import VoteSerializer
from ..models import Vote

log = logging.getLogger(__name__)


class ObjectRatingView(APIView):

    @transaction.atomic
    def get_vote(self, request, obj_ct, obj_uid):

        app_label, model = obj_ct.split(".")

        kwargs = {
            "content_type": ContentType.objects.get(app_label=app_label, model=model),
            f"{model}__uid": obj_uid,
        }
        if self.request.user.is_authenticated:
            kwargs.update(
                {
                    "user": self.request.user,
                }
            )
        else:
            kwargs.update(
                {
                    "user_identity": self.request.user_identity,
                }
            )

        try:
            return Vote.objects.get(**kwargs)

        except Vote.DoesNotExist:
            return None

    @transaction.atomic
    def create_vote(self, request, obj_ct, obj_uid, value, scope=None, comment=""):

        content_object = apps.get_model(*obj_ct.split(".")).objects.get(uid=obj_uid)

        kwargs = {
            "content_object": content_object,
            "value": value,
            "scope": scope,
            "comment": comment,
        }

        if self.request.user.is_authenticated:
            kwargs.update(
                {
                    "user": self.request.user,
                }
            )
        else:
            kwargs.update(
                {
                    "user_identity": self.request.user_identity,
                }
            )

        return Vote.objects.create(**kwargs)

    def get(self, request, obj_ct, obj_uid):

        vote = self.get_vote(request, obj_ct, obj_uid)

        # if not vote:
        #     raise Http404

        serializer = VoteSerializer(vote)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, obj_ct, obj_uid):

        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        value = request.data.get("value")
        scope = request.data.get("scope")
        comment = bleach.clean(request.data.get("comment", ""))

        vote = self.get_vote(request, obj_ct, obj_uid)

        if vote and value:
            vote.value = value
            if scope:
                vote.scope = scope
            if comment:
                vote.comment = comment
            vote.save()
        elif vote:
            vote.delete()
            vote = None
        elif value:
            vote = self.create_vote(request, obj_ct, obj_uid, value, scope, comment)

        serializer = VoteSerializer(vote)

        return Response(serializer.data)
