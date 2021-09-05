# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from catalog.api.serializers import MediaSerializer as CatalogMediaSerializer
from catalog.models import Playlist, Media
from ..models import Editor, Emission

SITE_URL = getattr(settings, "SITE_URL")

logger = logging.getLogger(__name__)


class ImageSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if not instance:
            return None

        data = {
            "file": instance.file.name,
            "path": instance.path,
            "url": instance.url,
            "rgb": instance.rgb,
        }

        return data


class EditorSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:editor-detail",
        lookup_field="uid",
    )

    name = serializers.CharField(
        source="display_name",
    )
    image = ImageSerializer(
        read_only=True,
    )

    class Meta:
        model = Editor
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "num_playlists",
            "image",
        ]


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):

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
    playlist = PlaylistSerializer(
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


class SchedulePlaylistSerializer(CatalogMediaSerializer):

    editor = EditorSerializer()

    class Meta:
        model = Playlist
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "duration",
            "editor",
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


class ProgramEmissionSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:emission-detail",
        lookup_field="uid",
    )

    playlist_uid = serializers.CharField(
        source="playlist.uid",
    )
    name = serializers.CharField(
        source="playlist.name",
    )
    series = serializers.CharField(
        source="playlist.series",
        allow_null=True,
    )
    series = serializers.CharField(
        source="playlist.series",
        allow_null=True,
    )
    series_episode = serializers.CharField(
        source="playlist.series_episode",
        allow_null=True,
    )
    editor = serializers.CharField(
        source="playlist.editor",
    )
    tags = serializers.StringRelatedField(
        source="playlist.tags",
        many=True,
    )

    class Meta:
        model = Emission
        fields = [
            "url",
            "ct",
            "uid",
            "playlist_uid",
            "name",
            "series",
            "series_episode",
            "editor",
            "tags",
            "duration",
            "time_start",
            "time_end",
        ]
