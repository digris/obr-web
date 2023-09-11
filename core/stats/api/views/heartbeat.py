from django.db.models.functions import Now

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from stats.api import serializers
from stats.models import Heartbeat


class HeartbeatView(
    APIView,
):
    def put(self, request):

        # NOTE: this is just a minimalistic serializer, as the only field we get from the
        #       client is `in_foreground`.
        #       to handle this situation in the same way as in other views we use a serializer here as well.
        serializer = serializers.HeartbeatCreateSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            heartbeat, _ = Heartbeat.objects.update_or_create(
                user_identity=request.user_identity,
                device_key=request.device_key,
                defaults={
                    "time": Now(),
                    "user_agent": request.headers.get("User-Agent", ""),
                }
                | serializer.validated_data,
            )

            return Response(
                None,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
