from api_extra.serializers import CTUIDModelSerializer
from catalog.models import Label, LabelImage
from image.api.serializers import BaseImageSerializer
from rest_framework import serializers


class LabelImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        model = LabelImage


class LabelSerializer(
    CTUIDModelSerializer,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:label-detail",
        lookup_field="uid",
    )
    name = serializers.CharField(
        read_only=True,
    )
    image = LabelImageSerializer(
        read_only=True,
        allow_null=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Label
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "name",
            "image",
        ]
