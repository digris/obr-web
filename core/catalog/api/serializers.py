# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers

from ..models import Mood, Artist, Media, MediaArtists, PlaylistMedia

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
            "rgb": instance.rgb,
        }

        return data

    class Meta:
        ref_name = "CatalogImageSerializer"


class MoodSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:mood-detail",
        lookup_field="uid",
    )

    class Meta:
        model = Mood
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "teaser",
        ]


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:artist-detail",
        lookup_field="uid",
    )

    image = ImageSerializer(read_only=True)

    num_media = serializers.IntegerField()

    user_rating = serializers.IntegerField(read_only=True, allow_null=True)

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
            "user_rating",
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


class UserRatingSerializer(serializers.Serializer):
    vote = serializers.IntegerField()


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
    releases = ReleaseSerializer(many=True, read_only=True)
    duration = DurationInSecondsSerializer(read_only=True)

    latest_airplay = serializers.DateTimeField(read_only=True, allow_null=True)

    num_airplays = serializers.IntegerField(read_only=True, allow_null=True)

    user_rating = serializers.IntegerField(read_only=True, allow_null=True)

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
            "releases",
            "duration",
            "latest_airplay",
            "num_airplays",
            "user_rating",
        ]


class PlaylistMediaSerializer(serializers.ModelSerializer):

    media = MediaSerializer(read_only=True)

    class Meta:
        model = PlaylistMedia
        fields = [
            "media",
            "position",
            "cue_in",
            "cue_out",
            "fade_in",
            "fade_out",
            "fade_cross",
        ]


# class PlaylistSeriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Series
#         fields = [
#             "name",
#         ]


class PlaylistSerializer(
    FlexFieldsSerializerMixin, serializers.HyperlinkedModelSerializer
):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:playlist-detail",
        lookup_field="uid",
    )

    image = ImageSerializer(read_only=True)
    latest_emission = serializers.DateTimeField(read_only=True)
    num_media = serializers.IntegerField(read_only=True)
    num_emissions = serializers.IntegerField(read_only=True)
    series = serializers.SerializerMethodField()
    user_rating = serializers.IntegerField(read_only=True, allow_null=True)

    def get_series(self, obj):
        if not obj.series:
            return None

        return {
            "ct": obj.series.ct,
            "uid": str(obj.series.uid),
            "name": obj.series.name if obj.series else None,
            "episode": obj.series_episode,
        }

    class Meta:
        model = Media
        ref_name = "CatalogPlaylistSerializer"
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "series",
            "latest_emission",
            "num_media",
            "num_emissions",
            "image",
            "user_rating",
        ]
        expandable_fields = {
            "media_set": (
                PlaylistMediaSerializer,
                {
                    "source": "playlist_media",
                    "many": True,
                },
            )
        }
