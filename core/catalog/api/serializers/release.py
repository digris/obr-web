from api_extra.serializers import CTUIDModelSerializer
from catalog.models import Release
from image.api.serializers import ImageSerializer
from rest_framework import serializers


class ReleaseSerializer(
    CTUIDModelSerializer,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:release-detail",
        lookup_field="uid",
    )
    name = serializers.CharField(
        read_only=True,
    )
    image = ImageSerializer(
        read_only=True,
    )
    num_media = serializers.IntegerField(
        read_only=True,
    )
    is_new = serializers.BooleanField(
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Release
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "name",
            "num_media",
            "is_new",
            "image",
        ]
