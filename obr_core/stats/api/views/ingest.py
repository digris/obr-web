import logging
from datetime import datetime

from django.utils import timezone

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from stats.api import permissions, serializers
from stats.models import PlayerEvent

logger = logging.getLogger(__name__)


class PlayerEventCreateView(
    APIView,
):
    @extend_schema(
        methods=["PUT"],
        operation_id="stats_player_event",
        description="""Ingest Player-event""",
        request=serializers.PlayerEventCreateSerializer(
            many=True,
        ),
        responses={
            201: None,
        },
    )
    def put(self, request):
        events = request.data.get("events", [])

        serializer = serializers.PlayerEventCreateSerializer(
            data=events,
            many=True,
        )

        if serializer.is_valid():
            for event_data in serializer.data:
                # NOTE: client / browser timestamps are not reliable ;)
                #       so we use timezone.now()

                now = timezone.now()

                ts = timezone.make_aware(
                    datetime.fromtimestamp(float(event_data["ts"]) / 1000.0),
                )

                logger.debug(f"now: {now} - ts-browser: {ts} - diff: {now - ts}")

                event = PlayerEvent(
                    source=event_data["source"],
                    state=event_data["state"],
                    obj_key=event_data["obj_key"],
                    time=now,
                    user_identity=request.user_identity,
                    device_key=request.device_key,
                )
                event.save()

            return Response(
                None,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class StreamEventCreateView(
    APIView,
):
    permission_classes = [
        permissions.EventCreatePermission,
    ]
    serializer_class = serializers.StreamEventSerializer

    @extend_schema(
        methods=["POST"],
        operation_id="stats_stream_event",
        description="""Ingest 'stream-events' from icecast server""",
        request=serializers.StreamEventSerializer,
        responses={
            201: None,
        },
    )
    def post(self, request):
        events = request.data

        serializer = serializers.StreamEventSerializer(
            data=events,
            many=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"created": len(events)},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
