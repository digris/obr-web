# -*- coding: utf-8 -*-
from rest_framework import serializers

from catalog.models import Media
from image.api.serializers import ImageSerializer


class ReleaseSerializer(
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:release-detail",
        lookup_field="uid",
    )
    image = ImageSerializer(
        read_only=True,
    )
    num_media = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Media
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "num_media",
            "image",
        ]
