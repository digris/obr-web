from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from broadcast.models import Emission
from catalog.models import Playlist
from image.api.serializers import ImageSerializer


class EmissionPlaylistSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:playlist-detail",
        lookup_field="uid",
    )

    image = ImageSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "image",
        ]


class EmissionMediaSerializer(serializers.Serializer):
    uid = serializers.CharField()
    cue_in = serializers.IntegerField()
    cue_out = serializers.IntegerField()
    fade_in = serializers.IntegerField()
    fade_out = serializers.IntegerField()
    fade_cross = serializers.IntegerField()
    time_start = serializers.DateTimeField()
    time_end = serializers.DateTimeField()


class EmissionSerializer(
    FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer
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
    media_set = EmissionMediaSerializer(
        source="get_media_set",
        many=True,
    )

    class Meta:
        model = Emission
        fields = [
            "url",
            "playlist",
            "ct",
            "uid",
            "time_start",
            "time_end",
            "duration",
            "media_set",
        ]
