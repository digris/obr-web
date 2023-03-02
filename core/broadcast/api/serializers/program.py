from api_extra.serializers import CTUIDModelSerializer
from broadcast.api.serializers import EditorSerializer
from broadcast.models import Emission
from catalog.api.serializers import PlaylistSerializer
from rest_framework import serializers
from tagging.api.serializers import TagSerializer


class ProgramEmissionPlaylistSerializer(PlaylistSerializer):
    class Meta(PlaylistSerializer.Meta):
        ref_name = "ProgramEmissionPlaylistSerializer"
        pass


class ProgramEmissionSerializer(
    CTUIDModelSerializer,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:emission-detail",
        lookup_field="uid",
    )
    playlist = ProgramEmissionPlaylistSerializer(
        fields=[
            "ct",
            "uid",
            "url",
            "name",
            "image",
        ],
        read_only=True,
    )
    name = serializers.CharField(
        read_only=True,
    )
    series = serializers.DictField(
        source="playlist.series_dict",
        allow_null=True,
        read_only=True,
    )
    editor = EditorSerializer(
        source="playlist.editor",
        allow_null=True,
        read_only=True,
    )
    tags = TagSerializer(
        source="playlist.tags",
        many=True,
        allow_null=True,
        read_only=True,
    )
    duration = serializers.DurationField(
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Emission
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "playlist",
            "name",
            "series",
            "editor",
            "tags",
            "duration",
            "time_start",
            "time_end",
        ]


class ProgramSerializer(serializers.Serializer):
    time_from = serializers.DateTimeField(
        read_only=True,
    )
    time_until = serializers.DateTimeField(
        read_only=True,
    )
    emissions = ProgramEmissionSerializer(
        many=True,
        read_only=True,
    )
