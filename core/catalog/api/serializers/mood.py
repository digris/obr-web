from rest_framework import serializers

from catalog.models import Mood
from tagging.api.serializers import TagSerializer


class MoodSerializer(
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:mood-detail",
        lookup_field="uid",
    )
    tags = TagSerializer(
        many=True,
    )

    class Meta:
        model = Mood
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "teaser",
            "tags",
            "animation_url",
        ]
