import logging
from itertools import chain

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

import dateutil.parser
from broadcast.api import serializers
from broadcast.models import Emission
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError
from stats.models import Emission as ArchivedEmission

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

    def get_time_filter(self):
        if time_from_str := self.request.query_params.get("time_from"):
            time_from = dateutil.parser.parse(time_from_str.replace(" ", "+"))
            if timezone.is_naive(time_from):
                time_from = timezone.make_aware(time_from)
        else:
            time_from = None

        if time_until_str := self.request.query_params.get("time_until"):
            time_until = dateutil.parser.parse(time_until_str.replace(" ", "+"))
            if timezone.is_naive(time_until):
                time_until = timezone.make_aware(time_until)
        else:
            time_until = None

        return time_from, time_until

    def get_queryset(self):
        # as we have data from different models we have to query them separately and
        # return as combined list
        qs = self.queryset.exclude(
            Q(time_start__isnull=True) | Q(time_end__isnull=True),
        ).select_related(
            "playlist",
        )
        archived_qs = ArchivedEmission.objects.exclude(
            Q(time_start__isnull=True) | Q(time_end__isnull=True),
        ).select_related(
            "playlist",
        )

        try:
            time_from, time_until = self.get_time_filter()
        except dateutil.parser.ParserError as e:
            raise ParseError(f"Invalid filter: {str(e)}") from e

        if time_from:
            qs = qs.filter(
                time_start__gte=time_from,
            )
            archived_qs = archived_qs.filter(
                time_start__gte=time_from,
            )

        if time_until:
            qs = qs.filter(
                time_end__lte=time_until,
            )
            archived_qs = archived_qs.filter(
                time_end__lte=time_until,
            )

        union_qs = list(chain(qs, archived_qs))

        union_qs = sorted(union_qs, key=lambda x: x.time_start, reverse=True)

        return union_qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        if obj := Emission.objects.filter(uid=obj_uid).first():
            return obj

        return get_object_or_404(ArchivedEmission, uid=obj_uid)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="expand",
                location=OpenApiParameter.QUERY,
                enum=["media_set", "live_ratings"],
                many=True,
            ),
            OpenApiParameter(
                name="time_from",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.DATETIME,
                pattern="YYYY-MM-DDTHH:MM:SS",
                examples=[
                    OpenApiExample(
                        "Date",
                        value="2023-03-07",
                    ),
                    OpenApiExample(
                        "Date & time",
                        value="2023-03-07T08:00:00",
                    ),
                    OpenApiExample(
                        "Date & time with Timezone",
                        value="2023-03-07T08:00:00+01:00",
                    ),
                ],
            ),
            OpenApiParameter(
                name="time_until",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.DATETIME,
                pattern="YYYY-MM-DDTHH:MM:SS",
                description="See `time_from` for examples.",
            ),
        ],
        responses={
            200: serializers.EmissionSerializer(
                many=True,
                expand=[
                    "live_ratings",
                    "media_set",
                ],
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
