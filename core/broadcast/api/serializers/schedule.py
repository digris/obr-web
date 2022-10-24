from rest_framework import serializers

from broadcast.api.serializers import EditorSerializer
from broadcast.models import Emission
from catalog.api.serializers import MediaSerializer as CatalogMediaSerializer
from catalog.api.serializers import PlaylistSerializer as CatalogPlaylistSerializer
from catalog.api.serializers.media import (
    MediaImageSerializer as CatalogMediaImageSerializer,
)
from catalog.models import Playlist, Media
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
    duration = serializers.DurationField(
        read_only=True,
    )

    class Meta:
        model = Playlist
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "duration",
            "editor",
            "series",
        ]


class ScheduleSerializer(serializers.Serializer):
    key = serializers.CharField(
        # read_only=True,
    )
    cue_in = serializers.IntegerField(
        # read_only=True,
    )
    cue_out = serializers.IntegerField(
        # read_only=True,
    )
    fade_in = serializers.IntegerField(
        # read_only=True,
    )
    fade_out = serializers.IntegerField(
        # read_only=True,
    )
    fade_cross = serializers.IntegerField(
        # read_only=True,
    )
    time_start = serializers.DateTimeField(
        # read_only=True,
    )
    time_end = serializers.DateTimeField(
        # read_only=True,
    )

    media = ScheduleMediaSerializer(
        # read_only=True,
    )
    emission = ScheduleEmissionSerializer(
        # read_only=True,
    )
    playlist = SchedulePlaylistSerializer(
        source="emission.playlist",
        # read_only=True,
    )
