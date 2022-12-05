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


class DurationInSecondsSerializer(
    serializers.Serializer,
):
    def to_representation(self, instance):
        if not isinstance(instance, timedelta):
            return 0

        return instance.seconds


class ReadOnlyModelSerializer(
    serializers.ModelSerializer,
):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setattr(self.Meta, "read_only_fields", list(self.fields))
