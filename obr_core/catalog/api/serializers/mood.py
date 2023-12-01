from api_extra.serializers import CTUIDModelSerializer
from catalog.models import Mood
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from tagging.api.serializers import TagSerializer


@extend_schema_field(
    {
        "type": "integer",
    },
)
class RGBValueField(
    serializers.FloatField,
):
    min_value = 0
    max_value = 255


# @extend_schema_field(OpenApiTypes.OBJECT)
class RayColorSerializer(serializers.Serializer):
    inner = serializers.ListField(
        child=RGBValueField(),
        min_length=4,
        max_length=4,
        read_only=True,
    )
    outer = serializers.ListField(
        child=RGBValueField(),
        min_length=4,
        max_length=4,
        read_only=True,
    )


class RaySerializer(serializers.Serializer):
    count = serializers.IntegerField()
    spread = serializers.FloatField()
    width = serializers.FloatField()
    length = serializers.IntegerField()
    colors = RayColorSerializer()


class MoodSerializer(
    CTUIDModelSerializer,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:mood-detail",
        lookup_field="uid",
    )
    name = serializers.CharField(
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    rgb = serializers.ListField(
        child=RGBValueField(),
        min_length=3,
        max_length=3,
        read_only=True,
    )
    rays = serializers.ListField(
        child=RaySerializer(),
        read_only=True,
    )
    user_rating = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Mood
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "name",
            "teaser",
            "tags",
            "rgb",
            "rays",
            "user_rating",
        ]
