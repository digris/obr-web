import copy
import uuid

from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, ref_name=None, read_only=False, **kwargs):

    if read_only:
        fields = {name: copy.copy(field) for name, field in fields.items()}
        for field in fields.values():
            field.read_only = True

    serializer_class = create_serializer_class(
        name=ref_name or f"inline_serializer_{uuid.uuid4()}",
        fields=fields,
    )

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


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
