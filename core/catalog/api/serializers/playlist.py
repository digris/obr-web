from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from base.api.serializers import CTUIDModelSerializer
from catalog.api.serializers import MediaSerializer
from broadcast.models.editor import Editor
from broadcast.models.emission import Emission
from catalog.models import Playlist, PlaylistMedia
from image.api.serializers import ImageSerializer
from tagging.api.serializers import TagSerializer


class DurationInSecondsSerializer(
    serializers.Serializer,
):
    def to_representation(self, instance):
        if not instance:
            return None

        return instance.seconds


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

    class Meta:
        model = Editor
        fields = [
            "url",
            "ct",
            "uid",
            "name",
        ]
        expandable_fields = {
            "image": (ImageSerializer),
        }


class PlaylistEmissionSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    class Meta:
        model = Emission
        fields = [
            "ct",
            "uid",
            "time_start",
            "time_end",
        ]


class PlaylistSerializer(
    FlexFieldsSerializerMixin,
    serializers.HyperlinkedModelSerializer,
):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:playlist-detail",
        lookup_field="uid",
    )
    image = ImageSerializer(
        read_only=True,
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
    num_emissions = serializers.IntegerField(
        read_only=True,
    )
    series = serializers.SerializerMethodField()
    user_rating = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )

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
        model = Playlist
        ref_name = "CatalogPlaylistSerializer"
        fields = [
            "url",
            "ct",
            "uid",
            "name",
            "series",
            "latest_emission_time_start",
            "user_rating_time_rated",
            "num_media",
            "num_emissions",
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
                },
            ),
            "tags": (
                TagSerializer,
                {
                    "many": True,
                },
            ),
            "duration": (DurationInSecondsSerializer,),
            "editor": (
                PlaylistEditorSerializer,
                {
                    "expand": ["image"],
                },
            ),
            "latest_emission": (PlaylistEmissionSerializer,),
        }
