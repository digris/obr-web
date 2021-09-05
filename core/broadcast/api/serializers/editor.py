# -*- coding: utf-8 -*-
from rest_framework import serializers

from broadcast.models import Editor
from image.api.serializers import ImageSerializer


class EditorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:editor-detail",
        lookup_field="uid",
    )

    name = serializers.CharField(
        source="display_name",
    )
    image = ImageSerializer(
        read_only=True,
    )

    class Meta:
        model = Editor
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "image",
        ]
