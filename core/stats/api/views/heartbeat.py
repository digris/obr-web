from django.db.models.functions import Now

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from stats.api import serializers
from stats.models import Heartbeat


class HeartbeatView(
    APIView,
):
    @extend_schema(
        methods=["PUT"],
        operation_id="stats_heartbeat",
        description="""Send Heartbeat""",
        request=serializers.HeartbeatCreateSerializer,
        responses={
            201: None,
        },
    )
    def put(self, request):
        # NOTE: this is just a minimalistic serializer, as the only field we get from the
        #       client is `in_foreground`.
        #       to handle this situation in the same way as in other views we use a serializer here as well.
        serializer = serializers.HeartbeatCreateSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            Heartbeat.objects.update_or_create(
                user_identity=request.user_identity,
                device_key=request.device_key,
                defaults={
                    "time": Now(),
                    "user_agent": request.headers.get("User-Agent", ""),
                    "remote_ip": request.remote_ip,
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
