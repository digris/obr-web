from rest_framework import serializers


class PageSerializer(
    serializers.Serializer,
):
    title = serializers.CharField(
        read_only=True,
    )
    summary = serializers.CharField(
        read_only=True,
    )
    body = serializers.CharField(
        read_only=True,
    )
