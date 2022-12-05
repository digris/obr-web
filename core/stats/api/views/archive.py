from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from stats.api import permissions, serializers
from stats.archive import archive_airplays, archive_emissions


class StatsArchiveView(
    APIView,
):
    permission_classes = [
        permissions.StatsAPIPermission,
    ]
    serializer_class = serializers.ArchiveSerializer

    @extend_schema(
        methods=["POST"],
        operation_id="stats_archive",
        description="""Archives `Emissions` & `Air-plays`.  
        This resource is periodically requested by GCP Cloud Scheduler.  
        Invoking requires `account.api_stats_webhooks` permissions.""",
    )
    def post(self, request):

        serializer = self.serializer_class(
            {
                "num_airplays_archived": archive_airplays(),
                "num_emissions_archived": archive_emissions(),
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
