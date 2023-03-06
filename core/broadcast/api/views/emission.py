import logging

from django.shortcuts import get_object_or_404
from django.utils import timezone

import dateutil.parser
from broadcast.api import serializers
from broadcast.models import Emission
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
        qs = self.queryset.select_related(
            "playlist",
        )
        archive_qs = ArchivedEmission.objects.all().select_related(
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
            archive_qs = archive_qs.filter(
                time_start__gte=time_from,
            )

        if time_until:
            qs = qs.filter(
                time_end__lte=time_until,
            )
            archive_qs = archive_qs.filter(
                time_end__lte=time_until,
            )

        combined_qs = list(qs) + list(archive_qs)

        combined_qs = sorted(combined_qs, key=lambda d: d.time_start)

        return combined_qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        if obj := Emission.objects.filter(uid=obj_uid).first():
            return obj

        return get_object_or_404(ArchivedEmission, uid=obj_uid)
