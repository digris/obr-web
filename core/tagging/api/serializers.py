from rest_framework import serializers
from tagging.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "ct",
            "uid",
            "type",
            "name",
        ]
