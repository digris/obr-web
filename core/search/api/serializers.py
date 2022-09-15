from rest_framework import serializers
from image.api.serializers import ImageSerializer


class SearchResultSerializer(serializers.Serializer):
    ct = serializers.CharField(
        read_only=True,
    )
    uid = serializers.CharField(
        read_only=True,
    )
    title = serializers.CharField(
        read_only=True,
    )
    subtitle = serializers.CharField(
        read_only=True,
    )
    image = ImageSerializer(
        read_only=True,
    )
