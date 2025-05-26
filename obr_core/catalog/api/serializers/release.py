from api_extra.serializers import CTUIDModelSerializer
from catalog.api.serializers.label import LabelSerializer
from catalog.models import Release, ReleaseImage
from image.api.serializers import BaseImageSerializer
from rest_framework import serializers


class ReleaseImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        model = ReleaseImage


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
    year = serializers.IntegerField(
        read_only=True,
        allow_null=True,
        source="release_year",
    )
    kind = serializers.CharField(
        read_only=True,
        source="release_type",
    )
    label = LabelSerializer(
        read_only=True,
        allow_null=True,
    )
    image = ReleaseImageSerializer(
        read_only=True,
        allow_null=True,
    )
    is_new = serializers.BooleanField(
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Release
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "name",
            "year",
            "kind",
            "is_new",
            "image",
            "label_display",
            "label",
        ]
