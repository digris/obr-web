from api_extra.serializers import CTUIDModelSerializer
from rest_framework import serializers
from tagging.models import Tag


class TagSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    name = serializers.CharField(read_only=True)

    class Meta(CTUIDModelSerializer.Meta):
        model = Tag
        fields = CTUIDModelSerializer.Meta.fields + [
            "type",
            "name",
        ]
