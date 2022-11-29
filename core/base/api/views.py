from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.conf import settings

from base import version
from base.utils.urls import get_absolute_url
from base.api import serializers


class VersionView(APIView):
    @staticmethod
    @extend_schema(
        responses={
            200: serializers.VersionSerializer,
        },
        operation_id="version",
    )
    def get(request):
        serializer = serializers.VersionSerializer(
            {
                "version": version.get_version(),
                "sha": version.get_short_sha(),
            },
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class SettingsView(APIView):
    @staticmethod
    @extend_schema(
        responses={
            200: serializers.SettingsSerializer,
        },
        operation_id="settings",
    )
    def get(request):
        serializer = serializers.SettingsSerializer(
            {
                "IMAGE_RESIZER_ENDPOINT": get_absolute_url(
                    request, settings.IMAGE_RESIZER_ENDPOINT
                ),
                "STREAM_ENDPOINTS": settings.STREAM_ENDPOINTS,
                "STREAM_LATENCY": settings.STREAM_LATENCY,
                "MEDIA_ENDPOINTS": settings.MEDIA_ENDPOINTS,
                "SENTRY_DSN": settings.SENTRY_DSN,
            },
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
