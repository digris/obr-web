import itertools
import logging

from django.utils import timezone

from api_extra.serializers import DurationInMillisecondsSerializer
from broadcast.api.utils import TIME_RANGE_PARAMETERS, get_time_range
from broadcast.models import Emission
from common.api.serializers import inline_serializer
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.views import APIView, Response

logger = logging.getLogger(__name__)

SCHEDULE_SECONDS_BACK = 60 * 30
SCHEDULE_SECONDS_AHEAD = 60 * 60


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
        parameters=TIME_RANGE_PARAMETERS,
        responses={
            200: OutputSerializer(
                many=False,
                read_only=True,
            ),
        },
    )
    def get(self, request):

        time_now = timezone.now().replace(microsecond=0)

        time_from, time_until = get_time_range(
            request,
            now=time_now,
            seconds_back=SCHEDULE_SECONDS_BACK,
            seconds_ahead=SCHEDULE_SECONDS_AHEAD,
        )

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
            e.get_media_set(include_all=True, for_playout=True) for e in qs
        )

        # and finally filter the media objects for the given time range
        items_in_range = [
            m
            for m in all_items
            if (m["time_end"] >= time_from and m["time_start"] <= time_until)
        ]

        items_in_range.sort(key=lambda i: i["time_start"])

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
