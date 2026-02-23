import datetime

from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from stats import export
from stats.api import permissions


class RadiodataLogUploadView(
    APIView,
):
    permission_classes = [
        permissions.WebhookPermission,
    ]

    class InputSerializer(serializers.Serializer):
        num_days = serializers.IntegerField(
            default=1,
            help_text="Number of days to upload, counting backwards from yesterday. Default: 1",
        )

    class OutputSerializer(serializers.Serializer):
        num_uploaded = serializers.IntegerField()

    @extend_schema(
        methods=["POST"],
        operation_id="stats_radiodata_log_upload",
        description="""Upload radio-data.ch logs.
        This resource is periodically requested by GCP Cloud Scheduler.
        Invoking requires `account.api_stats_webhooks` permissions.""",
    )
    def post(self, request):

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        num_days = input_serializer.validated_data["num_days"]

        today = datetime.date.today()
        date_until = today - datetime.timedelta(days=1)
        date_from = date_until - datetime.timedelta(days=num_days - 1)

        try:
            files_uploaded = export.radiodata_log_upload(
                date_from=date_from,
                date_until=date_until,
            )
        except export.ExporterError as e:
            return Response(
                {"detail": f"error uploading logs: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = self.OutputSerializer(
            {
                "num_uploaded": len(files_uploaded),
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
