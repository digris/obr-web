import itertools
import logging
from datetime import timedelta

from django.utils import timezone
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from broadcast.api import serializers
from broadcast.models import Emission

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100


class ScheduleView(GenericAPIView):
    serializer_class = serializers.ScheduleSerializer

    def get_queryset(self):
        qs = (
            Emission.objects.all()
            .select_related(
                "playlist",
                "playlist__editor",
                "playlist__series",
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
