from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from datetime import timedelta


@extend_schema_field(
    {
        "type": "integer",
    }
)
class RGBValueField(
    serializers.IntegerField,
):
    min_value = 0
    max_value = 255


class CTUIDModelSerializer(
    serializers.Serializer,
):
    uid = serializers.CharField(
        min_length=8,
        max_length=8,
        help_text="UID",
    )


class DurationInSecondsSerializer(
    serializers.Serializer,
):
    def to_representation(self, instance):
        if not isinstance(instance, timedelta):
            return 0

        return instance.seconds
