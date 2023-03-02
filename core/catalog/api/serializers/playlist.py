from api_extra.serializers import CTUIDModelSerializer, DurationInSecondsSerializer
from broadcast.models.editor import Editor
from broadcast.models.emission import Emission
from catalog.api.serializers import MediaSerializer
from catalog.models import Playlist, PlaylistMedia, PlaylistImage, Series
from image.api.serializers import BaseImageSerializer, ImageSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from tagging.api.serializers import TagSerializer


class PlaylistImageSerializer(BaseImageSerializer):
    class Meta(BaseImageSerializer.Meta):
        model = PlaylistImage


class PlaylistMediaSerializer(
    serializers.ModelSerializer,
):
    media = MediaSerializer(
        read_only=True,
    )

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


# TODO: find a better way to handle editor
class PlaylistEditorSerializer(
    CTUIDModelSerializer,
    FlexFieldsSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:editor-detail",
        lookup_field="uid",
    )

    name = serializers.CharField(
        source="display_name",
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Editor
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "name",
        ]
        expandable_fields = {
            "image": (ImageSerializer),
        }


class PlaylistEmissionSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:emission-detail",
        lookup_field="uid",
    )
    class Meta(CTUIDModelSerializer.Meta):
        model = Emission
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "time_start",
            "time_end",
        ]


class PlaylistSeriesSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    name = serializers.CharField(
        read_only=True,
    )
    episode = serializers.CharField(
        read_only=True,
        source="series_episode",
        default="",
    )

    class Meta:
        model = Series
        fields = [
            "ct",
            "uid",
            "name",
            "episode",
        ]


class PlaylistSerializer(
    CTUIDModelSerializer,
    FlexFieldsSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:playlist-detail",
        lookup_field="uid",
    )
    image = PlaylistImageSerializer(
        read_only=True,
        allow_null=True,
    )
    latest_emission_time_start = serializers.DateTimeField(
        read_only=True,
    )
    user_rating_time_rated = serializers.DateTimeField(
        read_only=True,
        # allow_null=True,
    )
    num_media = serializers.IntegerField(
        read_only=True,
    )
    # num_emissions = serializers.IntegerField(
    #     read_only=True,
    # )
    user_rating = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    series = PlaylistSeriesSerializer(
        read_only=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Playlist
        # ref_name = "CatalogPlaylistSerializer"
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "name",
            "series",
            "latest_emission_time_start",
            "user_rating_time_rated",
            "num_media",
            # "num_emissions",
            "image",
            "user_rating",
        ]
        expandable_fields = {
            "media_set": (
                PlaylistMediaSerializer,
                {
                    # "source": "airplayed_playlist_media",
                    "source": "playlist_media",
                    "many": True,
                    "read_only": True,
                },
            ),
            "tags": (
                TagSerializer,
                {
                    "many": True,
                    "read_only": True,
                },
            ),
            "duration": (
                DurationInSecondsSerializer,
                {
                    "read_only": True,
                },
            ),
            "editor": (
                PlaylistEditorSerializer,
                {
                    "read_only": True,
                    "expand": ["image"],
                },
            ),
            "latest_emission": (
                PlaylistEmissionSerializer,
                {
                    "read_only": True,
                },
            ),
            "emissions": (
                PlaylistEmissionSerializer,
                {
                    "source": "get_emissions",
                    "read_only": True,
                    "many": True,
                },
            ),
        }
