from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from broadcast.models import Emission
from api_extra.serializers import CTUIDModelSerializer
from catalog.api.serializers import MediaSerializer as CatalogMediaSerializer
from catalog.models import Playlist, Media
from image.api.serializers import ImageSerializer


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
    uid = serializers.CharField()
    # media_uid = serializers.CharField()
    cue_in = serializers.IntegerField()
    cue_out = serializers.IntegerField()
    fade_in = serializers.IntegerField()
    fade_out = serializers.IntegerField()
    fade_cross = serializers.IntegerField()
    time_start = serializers.DateTimeField()
    time_end = serializers.DateTimeField()
    media = EmissionMediaSerializer()


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
