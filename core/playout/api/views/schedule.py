import itertools
import logging
from datetime import timedelta

from django.utils import timezone

from broadcast.models import Emission
from drf_spectacular.utils import extend_schema
from playout.api import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)

SCHEDULE_SECONDS_AHEAD = 60 * 60


class ScheduleView(
    GenericAPIView,
):
    def get_queryset(self):
        qs = Emission.objects.select_related(
            "playlist",
        )
        return qs

    @extend_schema(
        responses={
            200: serializers.ScheduleSerializer(
                many=True,
            ),
        },
    )
    # @method_decorator(cache_page(5 * 60))
    def get(self, request):
        time_from = timezone.now()
        time_until = time_from + timedelta(seconds=SCHEDULE_SECONDS_AHEAD)

        # first we need to get the current (and eventually upcoming) emission(s)
        qs = self.get_queryset().filter(
            time_end__gte=time_from,
            time_start__lte=time_until,
        )

        # then we get all containing media objects
        all_media = itertools.chain.from_iterable(
            [e.get_media_set(include_all=True) for e in qs],
        )

        # and finally filter the media objects for the given time range
        media_in_range = [
            m
            for m in all_media
            if (m["time_end"] >= time_from and m["time_start"] <= time_until)
        ]

        media_in_range.sort(key=lambda i: i["time_start"])

        print(f"# range:\n{time_from:%H:%M:%S} - {time_until:%H:%M:%S}")

        print("# emissions")
        for e in qs:
            print(f"{e.time_start:%H:%M:%S} - {e.time_end:%H:%M:%S} : {e}")

        print("# media")
        for m in media_in_range:
            print(
                f"{m['time_start']:%H:%M:%S} - {m['time_end']:%H:%M:%S} : {m['media']}",
            )

        serializer = serializers.ScheduleSerializer(
            media_in_range,
            many=True,
            read_only=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)
