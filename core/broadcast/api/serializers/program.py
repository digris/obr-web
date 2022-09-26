from rest_framework import serializers

from api_extra.serializers import CTUIDModelSerializer
from tagging.api.serializers import TagSerializer
from catalog.api.serializers import PlaylistSerializer
from broadcast.api.serializers import EditorSerializer
from broadcast.models import Emission


class ProgramEmissionSerializer(
    CTUIDModelSerializer,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:emission-detail",
        lookup_field="uid",
    )
    playlist = PlaylistSerializer(
        fields=[
            "ct",
            "uid",
            "url",
            "name",
            "image",
        ]
    )
    name = serializers.CharField()
    series = serializers.DictField(
        source="playlist.series_dict",
        allow_null=True,
    )
    editor = EditorSerializer(
        source="playlist.editor",
        allow_null=True,
    )
    tags = TagSerializer(
        source="playlist.tags",
        many=True,
        allow_null=True,
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
    time_from = serializers.DateTimeField()
    time_until = serializers.DateTimeField()
    emissions = ProgramEmissionSerializer(
        many=True,
    )
