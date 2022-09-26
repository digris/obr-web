from rest_framework import serializers
from api_extra.serializers import RGBValueField

from api_extra.serializers import CTUIDModelSerializer
from catalog.models import Mood
from tagging.api.serializers import TagSerializer


# class RayColorsSerializer(serializers.Serializer):
#     inner = serializers.ListField(
#         child=RGBValueField(),
#         min_length=3,
#         max_length=3,
#         read_only=True,
#     )
#     outer = serializers.ListField(
#         child=RGBValueField(),
#         min_length=3,
#         max_length=3,
#         read_only=True,
#     )


class RaySerializer(serializers.Serializer):
    count = serializers.IntegerField()
    spread = serializers.FloatField()
    width = serializers.FloatField()
    length = serializers.IntegerField()
    # colors = RayColorsSerializer()
    colors = serializers.JSONField()


class MoodSerializer(
    CTUIDModelSerializer,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:mood-detail",
        lookup_field="uid",
    )
    tags = TagSerializer(
        many=True,
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
