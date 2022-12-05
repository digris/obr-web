from image.api.serializers import ImageSerializer
from rest_framework import serializers


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
    image = ImageSerializer(
        read_only=True,
    )
