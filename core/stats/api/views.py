import logging
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers


logger = logging.getLogger(__name__)


class PlayerEventView(APIView):
    serializer_class = serializers.PlayerEventSerializer

    def put(self, request):

        events = request.data.get("events", [])
        annotated_events = []

        for event in events:
            event["user_identity"] = request.user_identity
            event["device_key"] = request.device_key
            event["time"] = datetime.fromtimestamp(float(event["ts"]) / 1000.0)
            logger.info("player-event", event)
            annotated_events.append(event)

        serializer = self.serializer_class(
            data=annotated_events,
            many=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
