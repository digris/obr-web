# -*- coding: utf-8 -*-
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from catalog.models import Artist
from image.api.serializers import ImageSerializer
from tagging.api.serializers import TagSerializer


class ArtistSerializer(
    FlexFieldsSerializerMixin,
    serializers.ModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:artist-detail",
        lookup_field="uid",
    )
    image = ImageSerializer(
        read_only=True,
    )
    num_media = serializers.IntegerField(
        read_only=True,
    )
    user_rating = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Artist
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "num_media",
            "image",
            "country_code",
            "date_start",
            "date_end",
            "user_rating",
        ]
        expandable_fields = {
            "tags": (
                TagSerializer,
                {
                    "many": True,
                    "required": False,
                    "allow_null": True,
                },
            ),
        }