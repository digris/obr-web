# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from catalog.models import Playlist, Media
from catalog.api.serializers import MediaSerializer as CatalogMediaSerializer
from ..models import Emission

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
        }

        return data


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

    duration = serializers.DurationField(read_only=True)
    playlist = PlaylistSerializer(read_only=True)
    media_set = EmissionMediaSerializer(source="get_media_set", many=True)

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


# class ScheduleMediaSerializer(serializers.HyperlinkedModelSerializer):
#
#     url = serializers.HyperlinkedIdentityField(
#         view_name="api:catalog:media-detail",
#         lookup_field="uid",
#     )
#
#     class Meta:
#         model = Media
#         fields = [
#             "url",
#             "ct",
#             "uid",
#             "name",
#         ]


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
