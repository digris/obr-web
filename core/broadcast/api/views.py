# -*- coding: utf-8 -*-
import itertools
import logging
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from ..models import Emission

logger = logging.getLogger(__name__)


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

        # print(f"{time_from} - {time_until}")

        # get emissions within window
        qs = Emission.objects.filter(
            time_end__gte=time_from,
            time_start__lte=time_until,
        )

        # print(f"num: {qs.count()}")

        # print("// emissions ///")
        # for e in qs:
        #     print(f"e: {e.time_start} - {e.time_end}")

        flatten = itertools.chain.from_iterable

        all_media = flatten([e.get_media_set() for e in qs])
        media_in_range = [
            m
            for m in all_media
            if (m["time_end"] >= time_from and m["time_start"] <= time_until)
        ]

        # media_in_range = sorted(media_in_range, key=lambda i: i["time_start"])

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
