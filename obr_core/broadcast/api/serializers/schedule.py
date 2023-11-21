from broadcast.api.serializers import EditorSerializer
from broadcast.models import Emission
from catalog.api.serializers import MediaSerializer as CatalogMediaSerializer
from catalog.api.serializers import PlaylistSerializer as CatalogPlaylistSerializer
from catalog.api.serializers.media import (
    MediaImageSerializer as CatalogMediaImageSerializer,
)
from catalog.models import Media, Playlist
from rest_framework import serializers

from .emission import EmissionSerializer


class ScheduleMediaSerializer(CatalogMediaSerializer):
    image = CatalogMediaImageSerializer(
        read_only=True,
    )

    class Meta:
        model = Media
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "artist_display",
            "release_display",
            "artists",
            "releases",
            "duration",
            "image",
        ]


class ScheduleEmissionSerializer(EmissionSerializer):
    class Meta:
        model = Emission
        fields = [
            "url",
            "ct",
            "uid",
            "duration",
            "time_start",
            "time_end",
        ]


class SchedulePlaylistSerializer(CatalogPlaylistSerializer):
    editor = EditorSerializer(
        read_only=True,
    )
    series = serializers.JSONField(
        source="series_dict",
        read_only=True,
    )

    class Meta:
        model = Playlist
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            # "duration",
            "editor",
            "series",
        ]


class ScheduleSerializer(serializers.Serializer):
    key = serializers.CharField()
    cue_in = serializers.IntegerField()
    cue_out = serializers.IntegerField()
    fade_in = serializers.IntegerField()
    fade_out = serializers.IntegerField()
    fade_cross = serializers.IntegerField()
    time_start = serializers.DateTimeField()
    time_end = serializers.DateTimeField()

    media = ScheduleMediaSerializer()
    emission = ScheduleEmissionSerializer()
    playlist = SchedulePlaylistSerializer(
        source="emission.playlist",
    )

    # class Meta:
