# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_framework import serializers

from ..models import Artist, Media, MediaArtists


SITE_URL = getattr(settings, "SITE_URL")

logger = logging.getLogger(__name__)


class DurationInSecondsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if not instance:
            return None

        return instance.seconds


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


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:artist-detail",
        lookup_field="uid",
    )

    image = ImageSerializer(read_only=True)

    num_media = serializers.IntegerField()

    class Meta:
        model = Artist
        fields = [
            "url",
            "ct",
            # "uuid",
            "uid",
            "name",
            "num_media",
            "image",
        ]


class MediaArtistSerializer(serializers.ModelSerializer):

    # url = serializers.HyperlinkedIdentityField(
    #     source="artist.url",
    #     view_name="api:catalog:artist-detail",
    #     lookup_field="artist.uid",
    # )
    name = serializers.CharField(source="artist.name", read_only=True)
    ct = serializers.CharField(source="artist.ct", read_only=True)
    uid = serializers.CharField(source="artist.uid", read_only=True)

    class Meta:
        model = MediaArtists
        fields = [
            "ct",
            "uid",
            "name",
            "join_phrase",
        ]


class MediaSerializer(serializers.HyperlinkedModelSerializer):

    # controller_uuid = serializers.UUIDField(source="controller.uuid", read_only=True)

    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:media-detail",
        lookup_field="uid",
    )

    # state = serializers.ChoiceField(choices=Transmission.STATE_CHOICES)

    # time = serializers.DateTimeField(read_only=True)
    #
    # slide = SlideImageSerializer(read_only=True)
    #
    # events = TransmissionEventSerializer(many=True, read_only=True)

    artists = MediaArtistSerializer(source="media_artist", many=True, read_only=True)

    duration = DurationInSecondsSerializer(read_only=True)

    class Meta:
        model = Media
        fields = [
            "url",
            "ct",
            # "uuid",
            "uid",
            "name",
            "artist_display",
            "artists",
            "duration",
        ]


class ReleaseSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:release-detail",
        lookup_field="uid",
    )

    image = ImageSerializer(read_only=True)

    num_media = serializers.IntegerField(read_only=True)

    class Meta:
        model = Media
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "num_media",
            "image",
        ]


class PlaylistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:playlist-detail",
        lookup_field="uid",
    )

    image = ImageSerializer(read_only=True)

    num_media = serializers.IntegerField(read_only=True)
    num_emissions = serializers.IntegerField(read_only=True)

    class Meta:
        model = Media
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "num_media",
            "num_emissions",
            "image",
        ]
