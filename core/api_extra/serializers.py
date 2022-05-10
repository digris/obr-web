from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class CTUIDModelSerializer(serializers.Serializer):
    uid = serializers.CharField(
        min_length=8,
        max_length=8,
        help_text="UID",
    )


@extend_schema_field(
    {
        "type": "integer",
    }
)
class RGBValueField(serializers.IntegerField):
    min_value = 0
    max_value = 255
