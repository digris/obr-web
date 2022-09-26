from rest_framework import serializers
from api_extra.serializers import CTUIDModelSerializer
from tagging.models import Tag


class TagSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    class Meta(CTUIDModelSerializer.Meta):
        model = Tag
        fields = CTUIDModelSerializer.Meta.fields + [
            "type",
            "name",
        ]
