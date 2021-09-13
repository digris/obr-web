# -*- coding: utf-8 -*-
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from catalog.api.serializers.release import ReleaseSerializer
from catalog.models import Media, MediaArtists
from tagging.api.serializers import TagSerializer


class DurationInSecondsSerializer(
    serializers.Serializer,
):
    def to_representation(self, instance):
        if not instance:
            return None

        return instance.seconds


class MediaArtistSerializer(
    serializers.ModelSerializer,
):
    name = serializers.CharField(
        source="artist.name",
        read_only=True,
    )
    ct = serializers.CharField(
        source="artist.ct",
        read_only=True,
    )
    uid = serializers.CharField(
        source="artist.uid",
        read_only=True,
    )

    class Meta:
        model = MediaArtists
        fields = [
            "ct",
            "uid",
            "name",
            "join_phrase",
        ]


class MediaSerializer(
    FlexFieldsSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:media-detail",
        lookup_field="uid",
    )
    artists = MediaArtistSerializer(
        source="media_artist",
        many=True,
        read_only=True,
    )
    releases = ReleaseSerializer(
        many=True,
        read_only=True,
    )
    duration = DurationInSecondsSerializer(
        read_only=True,
    )
    latest_airplay = serializers.DateTimeField(
        read_only=True,
        allow_null=True,
    )
    num_airplays = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    user_rating = serializers.IntegerField(
        read_only=True,
        allow_null=True,
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
            "latest_airplay",
            "num_airplays",
            "user_rating",
        ]
        expandable_fields = {
            "tags": (
                TagSerializer,
                {
                    "many": True,
                },
            ),
        }
