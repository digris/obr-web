from api_extra.serializers import CTUIDModelSerializer
from rest_framework import serializers

from ..models import Category, Topic


class TopicSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    class Meta(CTUIDModelSerializer.Meta):
        model = Topic
        fields = CTUIDModelSerializer.Meta.fields + [
            "question",
            "answer",
        ]


class CategorySerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    topics = TopicSerializer(
        many=True,
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Category
        fields = CTUIDModelSerializer.Meta.fields + [
            "name",
            "topics",
        ]
