import itertools
import logging
from datetime import timedelta

from django.utils import timezone
from django.utils.decorators import method_decorator

import dateutil.parser
from broadcast.api import serializers
from broadcast.models import Emission
from common.cache.decorators import ignorable_cache_page
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework.exceptions import ParseError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100
SCHEDULE_MAX_RANGE = timedelta(hours=48)


def parse_datetime(value):
    # "+" in an un-encoded query-string arrives as " "
    dt = dateutil.parser.parse(value.replace(" ", "+"))
    return timezone.make_aware(dt) if timezone.is_naive(dt) else dt


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
            "playlist__editor__playlists",
        )
        return qs

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="secondsBack",
                type=OpenApiTypes.INT,
                description="Relative to now. Ignored if `timeFrom` is given.",
            ),
            OpenApiParameter(
                name="secondsAhead",
                type=OpenApiTypes.INT,
                description="Relative to now. Ignored if `timeUntil` is given.",
            ),
            OpenApiParameter(
                name="timeFrom",
                type=OpenApiTypes.DATETIME,
                description="Absolute, e.g. `2023-03-07T08:00:00+01:00`.",
            ),
            OpenApiParameter(
                name="timeUntil",
                type=OpenApiTypes.DATETIME,
                description="Absolute, see `timeFrom`.",
            ),
        ],
        responses={
            200: serializers.ScheduleSerializer(
                many=True,
            ),
        },
    )
    @method_decorator(ignorable_cache_page(60))
    def get(self, request):
        now = timezone.now()

        try:
            if value := request.GET.get("timeFrom"):
                time_from = parse_datetime(value)
            else:
                seconds_back = int(request.GET.get("secondsBack", 0))
                time_from = now - timedelta(seconds=seconds_back)

            if value := request.GET.get("timeUntil"):
                time_until = parse_datetime(value)
            else:
                seconds_ahead = int(request.GET.get("secondsAhead", 0))
                time_until = now + timedelta(seconds=seconds_ahead)
        except (ValueError, OverflowError) as e:
            raise ParseError(f"Invalid filter: {e}") from e

        if time_until - time_from > SCHEDULE_MAX_RANGE:
            raise ParseError(f"Range exceeds maximum of {SCHEDULE_MAX_RANGE}")

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
