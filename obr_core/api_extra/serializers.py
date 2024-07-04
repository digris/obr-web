from datetime import timedelta

from common.utils.urls import get_absolute_url
from drf_spectacular.utils import OpenApiTypes, extend_schema_field
from rest_framework import serializers


@extend_schema_field(
    {
        "type": "integer",
    },
)
class RGBValueField(
    serializers.IntegerField,
):
    min_value = 0
    max_value = 255


@extend_schema_field(
    {
        "type": "string",
    },
)
class AbsoluteURLField(
    serializers.URLField,
):
    def to_representation(self, value):
        if request := self.context.get("request"):
            return get_absolute_url(request, value)
        return value


class CTUIDSerializer(
    serializers.Serializer,
):
    ct = serializers.CharField(
        read_only=True,
        help_text="Content type",
    )
    uid = serializers.CharField(
        read_only=True,
        min_length=8,
        max_length=8,
        help_text="UID",
    )


class CTUIDModelSerializer(
    serializers.ModelSerializer,
):
    ct = serializers.CharField(
        read_only=True,
        help_text="Content type",
    )
    uid = serializers.CharField(
        read_only=True,
        min_length=8,
        max_length=8,
        help_text="UID",
    )

    class Meta:
        fields = [
            "ct",
            "uid",
        ]
        abstract = True


@extend_schema_field(
    OpenApiTypes.NUMBER,
)
class DurationInSecondsSerializer(
    serializers.Serializer,
):
    def to_representation(self, instance):
        if not isinstance(instance, timedelta):
            return 0

        return round(instance.total_seconds())


@extend_schema_field(
    OpenApiTypes.NUMBER,
)
class DurationInMillisecondsSerializer(
    serializers.Serializer,
):
    def to_representation(self, instance):
        if not isinstance(instance, timedelta):
            return 0

        return round(instance.total_seconds() * 1000)


class ReadOnlyModelSerializer(
    serializers.ModelSerializer,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.read_only_fields = list(self.fields)
