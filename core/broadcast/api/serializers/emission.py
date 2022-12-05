from api_extra.serializers import CTUIDModelSerializer
from broadcast.models import Emission
from catalog.api.serializers import MediaSerializer as CatalogMediaSerializer
from catalog.models import Media, Playlist
from image.api.serializers import ImageSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers


class EmissionPlaylistSerializer(
    CTUIDModelSerializer,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:playlist-detail",
        lookup_field="uid",
    )

    image = ImageSerializer(read_only=True)

    class Meta(CTUIDModelSerializer.Meta):
        model = Playlist
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "name",
            "image",
        ]


class EmissionMediaSerializer(
    CatalogMediaSerializer,
):
    class Meta:
        model = Media
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "artist_display",
            "artists",
            "releases",
            "duration",
        ]


class EmissionMediaSetSerializer(
    serializers.Serializer,
):
    uid = serializers.CharField(
        read_only=True,
    )
    cue_in = serializers.IntegerField(
        read_only=True,
    )
    cue_out = serializers.IntegerField(
        read_only=True,
    )
    fade_in = serializers.IntegerField(
        read_only=True,
    )
    fade_out = serializers.IntegerField(
        read_only=True,
    )
    fade_cross = serializers.IntegerField(
        read_only=True,
    )
    time_start = serializers.DateTimeField(
        read_only=True,
    )
    time_end = serializers.DateTimeField(
        read_only=True,
    )
    media = EmissionMediaSerializer(
        read_only=True,
    )


class EmissionSerializer(
    CTUIDModelSerializer,
    FlexFieldsSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:emission-detail",
        lookup_field="uid",
    )

    duration = serializers.DurationField(
        read_only=True,
    )
    playlist = EmissionPlaylistSerializer(
        read_only=True,
    )
    media_set = EmissionMediaSetSerializer(
        source="get_media_set",
        many=True,
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Emission
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "playlist",
            "time_start",
            "time_end",
            "duration",
            "media_set",
        ]
