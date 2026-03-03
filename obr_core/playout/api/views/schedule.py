import itertools
import logging
from datetime import timedelta

from django.utils import timezone

from api_extra.serializers import DurationInMillisecondsSerializer
from broadcast.models import Emission
from common.api.serializers import inline_serializer
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.views import APIView, Response

logger = logging.getLogger(__name__)

SCHEDULE_SECONDS_BACK = 60 * 60 * 0.5
SCHEDULE_SECONDS_AHEAD = 60 * 60 * 1


class ScheduleView(
    APIView,
):

    class OutputSerializer(serializers.Serializer):
        time_from = serializers.DateTimeField()
        time_until = serializers.DateTimeField()
        items = inline_serializer(
            many=True,
            fields={
                "uid": serializers.CharField(),
                "key": serializers.CharField(),
                "cue_in": serializers.IntegerField(),
                "cue_out": serializers.IntegerField(),
                "fade_in": serializers.IntegerField(),
                "fade_out": serializers.IntegerField(),
                "fade_cross": serializers.IntegerField(),
                "time_start": serializers.DateTimeField(),
                "time_end": serializers.DateTimeField(),
                "duration": DurationInMillisecondsSerializer(),
                "media": inline_serializer(
                    read_only=True,
                    fields={
                        "ct": serializers.CharField(),
                        "uid": serializers.CharField(),
                        "url": serializers.HyperlinkedIdentityField(
                            view_name="api:catalog:media-detail",
                            lookup_field="uid",
                        ),
                        "name": serializers.CharField(),
                        "duration": DurationInMillisecondsSerializer(),
                    },
                ),
                "master": inline_serializer(
                    source="media.master",
                    read_only=True,
                    fields={
                        "ct": serializers.CharField(),
                        "uid": serializers.CharField(),
                        "url": serializers.URLField(source="download_url"),
                        "size": serializers.IntegerField(),
                        "encoding": serializers.CharField(),
                        "content_type": serializers.CharField(),
                        "md5_hash": serializers.CharField(),
                        "path": serializers.CharField(),
                    },
                ),
                "emission": inline_serializer(
                    read_only=True,
                    fields={
                        "ct": serializers.CharField(),
                        "uid": serializers.CharField(),
                        "url": serializers.HyperlinkedIdentityField(
                            view_name="api:broadcast:emission-detail",
                            lookup_field="uid",
                        ),
                        "time_start": serializers.DateTimeField(),
                        "time_end": serializers.DateTimeField(),
                    },
                ),
                "playlist": inline_serializer(
                    source="emission.playlist",
                    read_only=True,
                    fields={
                        "ct": serializers.CharField(),
                        "uid": serializers.CharField(),
                        "url": serializers.HyperlinkedIdentityField(
                            view_name="api:catalog:playlist-detail",
                            lookup_field="uid",
                        ),
                        "name": serializers.CharField(),
                    },
                ),
            },
        )

        class Meta:
            ref_name = "PlayoutScheduleSerializer"

    @extend_schema(
        responses={
            200: OutputSerializer(
                many=False,
                read_only=True,
            ),
        },
    )
    # @method_decorator(cache_page(5 * 60))
    def get(self, request):

        time_now = timezone.now().replace(microsecond=0)

        time_from = time_now - timedelta(seconds=SCHEDULE_SECONDS_BACK)
        time_until = time_now + timedelta(seconds=SCHEDULE_SECONDS_AHEAD)

        #
        print(f"now:   {time_now}")
        print(f"from:  {time_from}")
        print(f"until: {time_until}")

        # first we need to get the current (and eventually upcoming) emission(s)
        qs = (
            Emission.objects.select_related(
                "playlist",
            )
            .filter(
                time_end__gte=time_from,
                time_start__lte=time_until,
            )
            .order_by("time_start")
        )

        # then we get all containing media objects
        all_items = itertools.chain.from_iterable(
            e.get_media_set(include_all=True) for e in qs
        )

        # and finally filter the media objects for the given time range
        items_in_range = [
            m
            for m in all_items
            if (m["time_end"] >= time_from and m["time_start"] <= time_until)
        ]

        items_in_range.sort(key=lambda i: i["time_start"])

        print(f"# range:\n  {time_from:%H:%M:%S} - {time_until:%H:%M:%S}")

        print("# emissions")
        for e in qs:
            is_current = e.time_start <= time_now < e.time_end
            print(
                f"{'*' if is_current else ' '} {e.time_start:%H:%M:%S} - {e.time_end:%H:%M:%S} : {e}",
            )

        print("# media")
        for m in items_in_range:
            is_current = m["time_start"] <= time_now < m["time_end"]
            print(
                f"{'*' if is_current else ' '} {m['time_start']:%H:%M:%S} - {m['time_end']:%H:%M:%S} : {m['media']}",
            )

        serializer = self.OutputSerializer(
            {
                "time_from": time_from,
                "time_until": time_until,
                "items": items_in_range,
            },
            read_only=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)
