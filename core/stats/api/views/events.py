import logging
from datetime import datetime

from django.utils import timezone

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from stats.models import PlayerEvent

from .. import serializers

logger = logging.getLogger(__name__)


class PlayerEventView(
    APIView,
):
    @extend_schema(
        methods=["PUT"],
        operation_id="stats_player_event",
        description="""Ingest Player-event""",
        request=serializers.PlayerEventCreateSerializer(many=True),
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
                event = PlayerEvent(
                    source=event_data["source"],
                    state=event_data["state"],
                    obj_key=event_data["obj_key"],
                    time=timezone.make_aware(
                        datetime.fromtimestamp(float(event_data["ts"]) / 1000.0)
                    ),
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
