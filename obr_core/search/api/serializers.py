from catalog.models.release import ReleaseImage as Image
from image.api.serializers import BaseImageSerializer
from rest_framework import serializers


class SearchResultImageSerializer(
    BaseImageSerializer,
):
    class Meta(BaseImageSerializer.Meta):
        model = Image


class SearchMediaResultSerializer(serializers.Serializer):
    ct = serializers.CharField(
        read_only=True,
    )
    uid = serializers.CharField(
        read_only=True,
    )
    title = serializers.CharField(
        read_only=True,
        source="name",
    )
    subtitle = serializers.CharField(
        read_only=True,
        source="artist_display",
    )
    image = SearchResultImageSerializer(
        read_only=True,
    )
