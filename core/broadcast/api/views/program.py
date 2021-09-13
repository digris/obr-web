# -*- coding: utf-8 -*-
import logging
from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from broadcast.api import serializers
from broadcast.models import Emission

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100


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
