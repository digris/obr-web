# -*- coding: utf-8 -*-
import itertools
import logging
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from ..models import Editor, Emission

logger = logging.getLogger(__name__)


class EditorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Editor.objects.all()
    serializer_class = serializers.EditorSerializer
    lookup_field = "uid"

    def get_queryset(self):
        qs = self.queryset.select_related("user")
        qs = qs.prefetch_related(
            "playlists",
            "images",
        )
        qs = qs.annotate(
            num_playlists=Count(
                "playlists",
            )
        )
        qs = qs.filter(
            num_playlists__gte=5,
        )
        qs = qs.order_by(
            Lower("display_name"),
        )
        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj


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
        except AssertionError:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj


class ScheduleView(APIView):
    @staticmethod
    def get(request):
        seconds_ahead = int(request.GET.get("seconds_ahead", 60 * 15))
        seconds_back = int(request.GET.get("seconds_back", 60 * 15))
        # NOTE: for the moment we just use a static "window"
        now = timezone.now()
        time_from = now - timedelta(seconds=seconds_ahead)
        time_until = now + timedelta(seconds=seconds_back)

        # get emissions within window
        qs = Emission.objects.filter(
            time_end__gte=time_from,
            time_start__lte=time_until,
        )

        flatten = itertools.chain.from_iterable

        all_media = flatten([e.get_media_set() for e in qs])
        media_in_range = [
            m
            for m in all_media
            if (m["time_end"] >= time_from and m["time_start"] <= time_until)
        ]

        media_in_range.sort(key=lambda i: i["time_start"], reverse=True)

        # print(len(media_set))
        #
        # for m in media_in_range:
        #     print(m["time_start"])

        serializer = serializers.ScheduleSerializer(
            media_in_range,
            many=True,
            read_only=True,
            context={"request": request},
        )

        return Response(serializer.data)
