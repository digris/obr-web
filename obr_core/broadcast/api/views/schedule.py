import itertools
import logging

from django.utils import timezone
from django.utils.decorators import method_decorator

from broadcast.api import serializers
from broadcast.api.utils import TIME_RANGE_PARAMETERS, get_time_range
from broadcast.models import Emission
from common.cache.decorators import ignorable_cache_page
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100


class ScheduleView(
    GenericAPIView,
):
    serializer_class = serializers.ScheduleSerializer

    def get_queryset(self):
        qs = Emission.objects.select_related(
            "playlist",
            "playlist__editor",
            "playlist__series",
        ).prefetch_related(
            "playlist__editor__images",
        )
        return qs

    @extend_schema(
        parameters=TIME_RANGE_PARAMETERS,
        responses={
            200: serializers.ScheduleSerializer(
                many=True,
            ),
        },
    )
    @method_decorator(ignorable_cache_page(60))
    def get(self, request):
        time_from, time_until = get_time_range(request, now=timezone.now())

        qs = self.get_queryset().filter(
            time_end__gte=time_from,
            time_start__lte=time_until,
        )

        flatten = itertools.chain.from_iterable

        all_media = flatten([e.get_media_set(include_all=True) for e in qs])
        media_in_range = [
            m
            for m in all_media
            if (m["time_end"] >= time_from and m["time_start"] <= time_until)
        ]

        media_in_range.sort(key=lambda i: i["time_start"], reverse=True)

        media_in_range = [m for m in media_in_range if m["media"].duration.seconds > 12]

        serializer = self.serializer_class(
            media_in_range,
            many=True,
            read_only=True,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)
