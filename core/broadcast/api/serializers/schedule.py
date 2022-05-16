from rest_framework import serializers

from broadcast.api.serializers import EditorSerializer
from broadcast.models import Emission
from catalog.api.serializers import MediaSerializer as CatalogMediaSerializer
from catalog.api.serializers import PlaylistSerializer as CatalogPlaylistSerializer
from catalog.models import Playlist, Media


class ScheduleMediaSerializer(CatalogMediaSerializer):
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


class ScheduleEmissionSerializer(CatalogMediaSerializer):
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
    editor = EditorSerializer()
    series = serializers.JSONField(source="series_dict")

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
