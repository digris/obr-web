# -*- coding: utf-8 -*-
import logging

from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from broadcast.api import serializers
from broadcast.models import Emission

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100


class EmissionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Emission.objects.all()
    serializer_class = serializers.EmissionSerializer
    lookup_field = "uid"

    def get_queryset(self):
        qs = self.queryset.select_related("playlist").prefetch_related(
            "playlist__images"
        )
        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj
