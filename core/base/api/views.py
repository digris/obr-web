from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .. import version


class VersionSerializer(serializers.Serializer):
    version = serializers.CharField(read_only=True, help_text="SemVer")
    sha = serializers.CharField(read_only=True, help_text="Git short SHA")


class VersionView(APIView):
    @staticmethod
    @extend_schema(
        responses={
            200: VersionSerializer,
        },
    )
    def get(request):
        data = {
            "version": version.get_version(),
            "sha": version.get_short_sha(),
        }
        return Response(
            data,
            status=status.HTTP_200_OK,
        )
