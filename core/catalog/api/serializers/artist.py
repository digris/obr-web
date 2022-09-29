from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from api_extra.serializers import CTUIDModelSerializer
from catalog.models import Artist
from image.api.serializers import ImageSerializer
from tagging.api.serializers import TagSerializer
from identifier.api.serializers import IdentifierSerializer
from api_extra.serializers import DurationInSecondsSerializer


class ArtistSerializer(
    CTUIDModelSerializer,
    FlexFieldsSerializerMixin,
    serializers.ModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:artist-detail",
        lookup_field="uid",
    )
    name = serializers.CharField(
        read_only=True,
    )
    image = ImageSerializer(
        read_only=True,
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
