import datetime
import logging

from django.utils import timezone

from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from stats import ingest
from stats.api import permissions

logger = logging.getLogger(__name__)


class ElasticsearchIngestView(
    APIView,
):
    permission_classes = [
        permissions.WebhookPermission,
    ]

    class InputSerializer(serializers.Serializer):
        num_days = serializers.IntegerField(
            default=1,
            help_text="Number of days to ingest, counting backwards from yesterday. Default: 1",
        )

    class OutputSerializer(serializers.Serializer):
        num_ingested = serializers.IntegerField()

    @extend_schema(
        methods=["POST"],
        operation_id="stats_elasticsearch_ingest",
        description="""Ingest Elasticsearch events.
        This resource is periodically requested by GCP Cloud Scheduler.
        Invoking requires `account.api_stats_webhooks` permissions.""",
    )
    def post(self, request):

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        num_days = input_serializer.validated_data["num_days"]

        now = timezone.localtime()

        anchor = now.replace(hour=4, minute=0, second=0, microsecond=0)

        if now < anchor:
            anchor -= datetime.timedelta(days=1)

        time_until = anchor
        time_from = anchor - datetime.timedelta(hours=num_days * 24 + 4)

        num_ingested = 0

        try:
            num_ingested += ingest.ingest_stream_sessions(
                time_from=time_from,
                time_until=time_until,
            )
        except ingest.IngestError as e:
            logger.warn(f"error ingesting stream sessions: {e}")

        try:
            num_ingested += ingest.ingest_player_sessions(
                time_from=time_from,
                time_until=time_until,
            )
        except ingest.IngestError as e:
            logger.warn(f"error ingesting player sessions: {e}")

        try:
            num_ingested += ingest.ingest_player_events(
                time_from=time_from,
                time_until=time_until,
            )
        except ingest.IngestError as e:
            logger.warn(f"error ingesting player events: {e}")

        serializer = self.OutputSerializer(
            {
                "num_ingested": num_ingested,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
