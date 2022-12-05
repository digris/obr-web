import logging
from datetime import datetime, timedelta
from itertools import chain

from django.db.models import Q
from django.utils import timezone

from broadcast.api import serializers
from broadcast.models import Emission
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from stats.models import Emission as ArchivedEmission

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100


class ProgramView(GenericAPIView):
    serializer_class = serializers.ProgramSerializer

    def get_emission_queryset(self):
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

    def get_archived_emission_queryset(self):
        qs = (
            ArchivedEmission.objects.all()
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="date",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.DATE,
                pattern="YYYY-MM-DD",
                description="""Defaults to the current date.  
                A day is considered to start at `06:00 CET`""",
            ),
        ],
    )
    def get(self, request):
        now = timezone.now()  # UTC
        if date := request.query_params.get("date"):
            now = datetime.strptime(date, "%Y-%m-%d")
        else:
            now = timezone.now()  # UTC

        # we want to set start / end in naive / local time for offset calculations
        if timezone.is_naive(now):
            naive = now
        else:
            naive = timezone.make_naive(now)

        naive_time_from = naive.replace(hour=6, minute=0, second=0, microsecond=0)
        time_from = timezone.make_aware(naive_time_from)  # now with timezone - CE(S)T)
        time_until = time_from + timedelta(seconds=60 * 60 * 24 - 1)  # 24h - 1s

        qs = (
            self.get_emission_queryset()
            .filter(Q(time_start__gte=time_from) & Q(time_start__lte=time_until))
            .order_by(
                "time_start",
            )
        )

        archived_qs = (
            self.get_archived_emission_queryset()
            .filter(Q(time_start__gte=time_from) & Q(time_start__lte=time_until))
            .order_by(
                "time_start",
            )
        )

        if qs.count() + archived_qs.count() > PROGRAM_MAX_EMISSIONS:
            return Response(
                {
                    "message": f"Too many emissions in range. Count: {qs.count()} - max: {PROGRAM_MAX_EMISSIONS}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        union_qs = list(chain(qs, archived_qs))

        union_qs = sorted(union_qs, key=lambda x: x.time_start)

        print(union_qs)

        serializer = self.serializer_class(
            {
                "time_from": time_from,
                "time_until": time_until,
                "emissions": union_qs,
            },
            context={
                "request": request,
            },
        )

        return Response(serializer.data)
