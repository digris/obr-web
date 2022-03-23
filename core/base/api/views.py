from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import version


class VersionView(APIView):
    def get(self, request):
        data = {
            "version": version.get_version(),
            "sha": version.get_short_sha(),
        }
        return Response(
            data,
            status=status.HTTP_200_OK,
        )
