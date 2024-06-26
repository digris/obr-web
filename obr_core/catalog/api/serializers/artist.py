from api_extra.serializers import (
    AbsoluteURLField,
    CTUIDModelSerializer,
    DurationInSecondsSerializer,
)
from catalog.models import Artist, ArtistImage
from identifier.api.serializers import IdentifierSerializer
from image.api.serializers import BaseImageSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from tagging.api.serializers import TagSerializer


class ArtistImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        model = ArtistImage


class ArtistSerializer(
    CTUIDModelSerializer,
    FlexFieldsSerializerMixin,
    serializers.ModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:artist-detail",
        lookup_field="uid",
    )
    detail_url = AbsoluteURLField(
        source="get_absolute_url",
    )
    name = serializers.CharField(
        read_only=True,
    )
    image = ArtistImageSerializer(
        read_only=True,
        allow_null=True,
    )
    num_media = serializers.IntegerField(
        read_only=True,
    )
    media_total_duration = DurationInSecondsSerializer(
        read_only=True,
    )
    user_rating = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Artist
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "detail_url",
            "name",
            "num_media",
            "media_total_duration",
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
            "identifiers": (
                IdentifierSerializer,
                {
                    "many": True,
                    "required": False,
                    "allow_null": True,
                },
            ),
        }
