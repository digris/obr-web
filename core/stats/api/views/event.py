import logging
from datetime import timedelta

from catalog.models import Media
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from stats.api import permissions, serializers
from stats.models import PlayerEvent, StreamEvent

logger = logging.getLogger(__name__)


class PlayerEventFilter(
    filters.FilterSet,
):
    for_year = filters.NumberFilter(
        field_name="time",
        lookup_expr="year",
    )
    time_from = filters.DateTimeFilter(
        field_name="time",
        lookup_expr="gt",
    )

    class Meta:
        model = PlayerEvent
        fields = [
            "source",
        ]


class PlayerEventViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = PlayerEvent.objects.all()
    serializer_class = serializers.PlayerEventSerializer

    permission_classes = [
        permissions.ViewPermission,
    ]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlayerEventFilter

    def get_queryset(self):
        qs = PlayerEvent.objects.filter(
            state="playing",
            duration__gt=timedelta(seconds=5),
        )

        return qs

    @staticmethod
    def override_media_durations(qs):
        media_uids = [e.obj_key[-8:] for e in qs]
        media_qs = Media.objects.filter(uid__in=media_uids)
        media_durations = {m.uid: m.duration for m in media_qs}

        # NOTE: this is rather ugly, consider as a temporary solution...
        #       it can happen that a play event has no close enough end time (no subsequent event)
        #       e.g. if the network disconnected, browser closed etc.
        #       so if the calculated event duration is longer than the media duration we just override it
        #       with the media duration.

        for event in qs:
            media_uid = event.obj_key[-8:]
            media_duration = media_durations[media_uid]
            if event.duration.total_seconds() > media_duration.total_seconds() + 5:
                logger.debug(
                    f"fix duration for {media_uid} - {event.duration.seconds} > {media_duration.seconds}",
                )
                # NOTE: yes - i know, this is ugly. see above...
                event.duration = media_duration

        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        page = self.override_media_durations(page)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StreamEventFilter(
    filters.FilterSet,
):
    for_year = filters.NumberFilter(
        field_name="time_start",
        lookup_expr="year",
    )
    time_from = filters.DateTimeFilter(
        field_name="time_start",
        lookup_expr="gt",
    )

    class Meta:
        model = StreamEvent
        fields = [
            "path",
        ]


class StreamEventViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = StreamEvent.objects.filter(bytes_sent__gt=1024)
    serializer_class = serializers.StreamEventSerializer

    permission_classes = [
        permissions.ViewPermission,
    ]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StreamEventFilter
