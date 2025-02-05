from rest_framework import serializers


class VersionSerializer(
    serializers.Serializer,
):
    version = serializers.CharField(
        read_only=True,
        help_text="SemVer",
    )
    sha = serializers.CharField(
        read_only=True,
        help_text="Git short SHA",
    )


class StreamEndpointsSerializer(
    serializers.Serializer,
):
    dash = serializers.CharField(
        read_only=True,
    )
    hls = serializers.CharField(
        read_only=True,
    )
    icecast = serializers.CharField(
        read_only=True,
    )
    news = serializers.CharField(
        read_only=True,
    )


class MediaEndpointsSerializer(
    serializers.Serializer,
):
    dash = serializers.CharField(
        read_only=True,
    )
    hls = serializers.CharField(
        read_only=True,
    )


class SettingsSerializer(
    serializers.Serializer,
):
    IMAGE_RESIZER_ENDPOINT = serializers.URLField(
        read_only=True,
    )
    STREAM_ENDPOINTS = StreamEndpointsSerializer(
        read_only=True,
    )
    STREAM_LATENCY = serializers.FloatField(
        read_only=True,
    )
    MEDIA_ENDPOINTS = MediaEndpointsSerializer(
        read_only=True,
    )
    SENTRY_DSN = serializers.CharField(
        read_only=True,
    )
