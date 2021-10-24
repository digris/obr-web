# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from catalog.api import serializers
from catalog.models import Mood

MEDIA_MIN_DURATION = 12


class MoodViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Mood.objects.all().order_by("name")
    serializer_class = serializers.MoodSerializer
    lookup_field = "uid"

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError:  # pragma: no cover
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj
