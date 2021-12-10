from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


@extend_schema_field(
    {
        "type": "integer",
    }
)
class RGBValueField(serializers.IntegerField):
    min_value = 0
    max_value = 255


class BaseImageSerializer(serializers.ModelSerializer):

    file = serializers.CharField(
        source="file.name",
        read_only=True,
        allow_null=True,
    )

    rgb = serializers.ListField(
        child=RGBValueField(),
        min_length=3,
        max_length=3,
        read_only=True,
    )

    class Meta:
        fields = [
            "uid",
            "path",
            "file",
            "rgb",
        ]
        abstract = True


class ImageSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if not instance:
            return None

        data = {
            "file": instance.file.name,
            "path": instance.path,
            "url": instance.url,
            "rgb": instance.rgb,
        }

        return data
