# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import VoteSerializer
from ..models import Vote

log = logging.getLogger(__name__)


class ObjectRatingView(APIView):
    def get_object(self, obj_ct, obj_uid):
        # print("**", obj_ct, obj_uid)

        qs = apps.get_model(*obj_ct.split("."))

        # # annotate with request user's rating
        # if self.request.user.is_authenticated:
        #     qs = qs.annotate(
        #         user_rating=Max(
        #             "votes__value", filter=Q(votes__user=self.request.user)
        #         ),
        #     )
        # # annotate with anonymous user 'identity'
        # else:
        #     qs = qs.annotate(
        #         user_rating=Max(
        #             "votes__value",
        #             filter=Q(votes__user_identity=self.request.user_identity),
        #         ),
        #     )

        try:
            obj = (
                apps.get_model(*obj_ct.split("."))
                .objects.prefetch_related("votes")
                .get(uid=obj_uid)
            )
            return obj

        except ObjectDoesNotExist:
            raise Http404

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

    def create_vote(self, request, obj_ct, obj_uid, value):

        content_object = apps.get_model(*obj_ct.split(".")).objects.get(uid=obj_uid)

        kwargs = {
            "content_object": content_object,
            "value": value,
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

        serializer = VoteSerializer(vote)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, obj_ct, obj_uid):

        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        value = request.data.get("value")
        vote = self.get_vote(request, obj_ct, obj_uid)

        if vote and value:
            vote.value = value
            vote.save()
        elif vote:
            vote.delete()
            vote = None
        elif value:
            vote = self.create_vote(request, obj_ct, obj_uid, value)

        serializer = VoteSerializer(vote)

        return Response(serializer.data)

    # def delete(self, request, pk):
    #     vote = self.get_object(pk)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


"""
from django.apps import apps
obj_ct = 'catalog.media'
from rating.models import Vote
from django.contrib.contenttypes.models import ContentType
app_label, model = obj_ct.split(".")
ct = ContentType.objects.get(app_label=app_label, model=model)
Vote.objects.filter(content_type=ct)
from account.models import User
u = User.objects.get(id=1)
Vote.objects.filter(content_type=ct, media__uid='F2B68907', user=u)
Vote.objects.get(content_type=ct, media__uid='F2B68907', user=u)
"""
