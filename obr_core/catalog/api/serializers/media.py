from api_extra.serializers import (
    AbsoluteURLField,
    CTUIDModelSerializer,
    DurationInSecondsSerializer,
)
from catalog.api.serializers.release import ReleaseSerializer
from catalog.models import Media, MediaArtists
from catalog.models.release import ReleaseImage as Image
from identifier.api.serializers import IdentifierSerializer
from image.api.serializers import BaseImageSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from tagging.api.serializers import TagSerializer


class MediaImageSerializer(
    BaseImageSerializer,
):
    class Meta(BaseImageSerializer.Meta):
        model = Image


class MediaArtistSerializer(
    serializers.ModelSerializer,
):
    url = serializers.HyperlinkedRelatedField(
        read_only=True,
        lookup_field="uid",
        source="artist",
        view_name="api:catalog:artist-detail",
    )
    name = serializers.CharField(
        source="artist.name",
        read_only=True,
    )
    ct = serializers.CharField(
        source="artist.ct",
        read_only=True,
    )
    uid = serializers.CharField(
        source="artist.uid",
        read_only=True,
    )

    class Meta:
        model = MediaArtists
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "join_phrase",
        ]


class MediaSerializer(
    CTUIDModelSerializer,
    FlexFieldsSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:media-detail",
        lookup_field="uid",
    )
    detail_url = AbsoluteURLField(
        source="get_absolute_url",
    )
    name = serializers.CharField(
        read_only=True,
    )
    artists = MediaArtistSerializer(
        source="media_artist",
        many=True,
        read_only=True,
    )
    artist_display = serializers.CharField(
        read_only=True,
    )
    release_display = serializers.CharField(
        read_only=True,
    )
    label_display = serializers.CharField(
        read_only=True,
    )
    releases = ReleaseSerializer(
        many=True,
        read_only=True,
    )
    duration = DurationInSecondsSerializer(
        read_only=True,
        help_text="in seconds",
    )
    latest_airplay = serializers.DateTimeField(
        read_only=True,
        allow_null=True,
    )
    num_airplays = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    user_rating = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    fade_in = serializers.IntegerField(
        read_only=True,
        default=0,
    )
    fade_out = serializers.IntegerField(
        read_only=True,
        default=0,
    )
    cue_in = serializers.IntegerField(
        read_only=True,
        default=0,
    )
    cue_out = serializers.IntegerField(
        read_only=True,
        default=0,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Media
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "detail_url",
            "name",
            "artist_display",
            "release_display",
            "label_display",
            "artists",
            "releases",
            "duration",
            "latest_airplay",
            "num_airplays",
            "user_rating",
            "fade_in",
            "fade_out",
            "cue_in",
            "cue_out",
        ]
        expandable_fields = {
            "image": (
                MediaImageSerializer,
                {
                    "required": False,
                },
            ),
            "tags": (
                TagSerializer,
                {
                    "many": True,
                    "required": False,
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
