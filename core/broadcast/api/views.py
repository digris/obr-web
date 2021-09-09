# -*- coding: utf-8 -*-
import itertools
import logging
from datetime import timedelta

from django.db.models import Count, Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, viewsets, status
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from . import serializers
from ..models import Editor, Emission

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100


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


class ScheduleView(GenericAPIView):

    serializer_class = serializers.ScheduleSerializer

    def get_queryset(self):
        qs = (
            Emission.objects.all()
            .select_related(
                "playlist",
                "playlist__editor",
            )
            .prefetch_related(
                "playlist__editor__images",
                "playlist__editor__playlists",
            )
        )
        return qs

    def get(self, request):
        seconds_ahead = int(request.GET.get("secondsAhead", 60 * 15))
        seconds_back = int(request.GET.get("secondsBack", 60 * 15))

        now = timezone.now()
        time_from = now - timedelta(seconds=seconds_ahead)
        time_until = now + timedelta(seconds=seconds_back)

        qs = self.get_queryset().filter(
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

        serializer = self.serializer_class(
            media_in_range,
            many=True,
            read_only=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)


class ProgramView(GenericAPIView):

    serializer_class = serializers.ProgramSerializer

    def get_queryset(self):
        qs = (
            Emission.objects.all()
            .select_related(
                "playlist",
                "playlist__editor",
                "playlist__series",
            )
            .prefetch_related(
                "playlist__tags",
            )
        )
        return qs

    def get(self, request):
        now = timezone.now()  # UTC
        # we want to set start / end in naive / local time
        naive = timezone.make_naive(now)
        naive_time_from = naive.replace(hour=6, minute=0, second=0, microsecond=0)
        time_from = timezone.make_aware(naive_time_from)  # now with timezone - CE(S)T)
        time_until = time_from + timedelta(seconds=60 * 60 * 24 - 1)  # 24h - 1s

        qs = (
            self.get_queryset()
            .filter(Q(time_start__gte=time_from) & Q(time_start__lte=time_until))
            .order_by(
                "time_start",
            )
        )

        if qs.count() > PROGRAM_MAX_EMISSIONS:
            return Response(
                {
                    "message": f"Too many emissions in range. Count: {qs.count()} - max: {PROGRAM_MAX_EMISSIONS}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(
            {
                "time_from": time_from,
                "time_until": time_until,
                "emissions": qs,
            },
            context={
                "request": request,
            },
        )

        return Response(serializer.data)
