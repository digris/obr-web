import logging
from datetime import datetime, timedelta

from broadcast.sync.schedule import sync_schedule
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from sync.update import update_by_app

from . import permissions, serializers

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
            num_hours = serializer.data.get("num_hours") or 4
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


class SyncAppView(
    APIView,
):
    permission_classes = [
        permissions.SyncAPIPermission,
    ]
    serializer_class = serializers.SyncAppSerializer

    @extend_schema(
        methods=["POST"],
        operation_id="sync_app",
        description="""Synchronize sync-enabled models with remote data.  
        This resource is periodically requested by GCP Cloud Scheduler.  
        Invoking requires `account.api_sync_webhooks` permissions.""",
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
        )

        if serializer.is_valid():
            app_labels = serializer.data["app_labels"]
            limit = serializer.data["limit"]
            max_age = serializer.data["max_age"]

            results = []
            for app_label in app_labels:
                results += update_by_app(
                    app_label=app_label,
                    max_age=max_age,
                    limit=limit,
                )

            response = {
                "updated": [{r[0]: r[1]} for r in results],
            }

            return Response(
                response,
                status=status.HTTP_202_ACCEPTED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
