# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import logging

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.apps import apps
from django.db import models
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist


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

    # def get_rating(self, obj, user):
    #
    #     avg_rating = {
    #         "avg_rating": None,
    #         "num_ratings": None,
    #         "user_rating": None,
    #     }
    #
    #     qs = obj.ratings.all()
    #
    #     if not qs.exists():
    #         return avg_rating
    #
    #     _r = qs.aggregate(rating=models.Avg("value"))
    #
    #     avg_rating["avg_rating"] = round(_r["rating"], 1)
    #     # avg_rating['avg_rating'] = _r['rating']
    #     avg_rating["num_ratings"] = qs.count()
    #
    #     if user.is_authenticated:
    #         try:
    #             _ur = obj.ratings.get(user=user)
    #             avg_rating["user_rating"] = _ur.value
    #         except ObjectDoesNotExist:
    #             pass
    #
    #     return avg_rating

    def get(self, request, obj_ct, obj_uid):

        # obj = self.get_object(obj_ct, obj_uid)
        # avg_rating = self.get_rating(obj, request.user)

        app_label, model = obj_ct.split(".")
        # ct = ContentType.objects.get(app_label=app_label, model=model)

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
            qs = Vote.objects.get(**kwargs)
            serializer = VoteSerializer(qs)
            return Response(serializer.data)

        except Vote.DoesNotExist:
            return Response({}, status=status.HTTP_200_OK)

    def put(self, request, obj_ct, obj_uid):

        return Response({})

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
