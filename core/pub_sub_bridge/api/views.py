# -*- coding: utf-8 -*-
import logging
from datetime import timedelta, datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class BridgeView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @staticmethod
    def post(request):
        # TODO: change this to url=mapping instead of RPC-style...
        payload = request.data
        command = payload.get("command")
        if command:
            print(f"run command: {command}")

            result = {}

            if command == "sync_schedule":
                # pylint: disable=import-outside-toplevel
                from sync import utils

                date_start = datetime.now().replace(minute=0, second=0)
                date_end = date_start + timedelta(hours=4)

                updated = list(
                    utils.sync_schedule(
                        date_start=date_start, date_end=date_end, force=True
                    )
                )

                # TODO: find a better place to update airplays...
                from catalog.sync.airplay import sync_airplays
                from catalog.models.media import Airplay

                sync_airplays(time_start=Airplay.objects.latest().time_end)

                result.update({"updated": [str(u) for u in updated]})

            return Response(result)

        return Response(payload)