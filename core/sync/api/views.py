import logging
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from broadcast.sync.schedule import sync_schedule

from . import serializers, permissions


logger = logging.getLogger(__name__)


class SyncScheduleView(
    APIView,
):
    permission_classes = [
        permissions.SyncAPIPermission,
    ]
    serializer_class = serializers.SyncScheduleSerializer

    @extend_schema(
        methods=["POST"],
        operation_id="sync_schedule",
        description="""Synchronize schedule with scheduler planning data.  
        This resource is periodically requested by GCP Cloud Scheduler""",
    )
    def post(self, request):

        serializer = self.serializer_class(
            data=request.data,
        )

        if serializer.is_valid():
            data = serializer.data

            num_hours = data.get("num_hours") or 4
            date_start = datetime.now().replace(minute=0, second=0, microsecond=0)
            date_end = date_start + timedelta(hours=num_hours)

            updated = list(
                sync_schedule(
                    date_start=date_start,
                    date_end=date_end,
                    force=True,
                )
            )

            response = {
                "num_updated": len(updated),
            }

            return Response(
                response,
                status=status.HTTP_202_ACCEPTED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
