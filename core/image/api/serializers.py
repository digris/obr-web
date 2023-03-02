from api_extra.serializers import CTUIDModelSerializer, RGBValueField
from rest_framework import serializers


class BaseImageSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    path = serializers.CharField(
        read_only=True,
        help_text="To be used with `IMAGE_RESIZER_ENDPOINT`",
    )

    url = serializers.URLField(
        read_only=True,
        help_text='"Internal" storage backend URL',
    )

    # ratio = serializers.IntegerField(
    #     read_only=True,
    #     help_text="Aspect ratio - e.g. `1.78` (16/9)",
    # )

    rgb = serializers.ListField(
        child=RGBValueField(),
        min_length=3,
        max_length=3,
        read_only=True,
    )

    class Meta:
        fields = CTUIDModelSerializer.Meta.fields + [
            "path",
            "url",
            # "ratio",
            "rgb",
        ]
        abstract = True


class ImageSerializer(
    serializers.Serializer,
):
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
