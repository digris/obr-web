import logging
from datetime import timedelta, datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

logger = logging.getLogger(__name__)


class BridgeView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    @extend_schema(
        # NOTE: add schema declaration if view will still be needed
        request=None,
        responses={
            200: None,
        },
        methods=["POST"],
    )
    def post(request):
        # TODO: change this to url=mapping instead of RPC-style...
        payload = request.data
        command = payload.get("command")
        if command:
            print(f"run command: {command}")

            result = {}

            if command == "sync_schedule":
                # pylint: disable=import-outside-toplevel
                from broadcast.sync import schedule

                date_start = datetime.now().replace(minute=0, second=0, microsecond=0)
                date_end = date_start + timedelta(hours=4)

                updated = list(
                    schedule.sync_schedule(
                        date_start=date_start, date_end=date_end, force=True
                    )
                )

                result.update({"updated": [str(u) for u in updated]})

            return Response(result)

        return Response(payload)
