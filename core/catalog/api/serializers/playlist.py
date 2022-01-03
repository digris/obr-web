from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from base.api.serializers import CTUIDModelSerializer
from catalog.api.serializers import MediaSerializer
from broadcast.models.editor import Editor
from catalog.models import Media, PlaylistMedia
from image.api.serializers import ImageSerializer
from tagging.api.serializers import TagSerializer


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
    latest_emission = serializers.DateTimeField(
        read_only=True,
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
            ),
            "tags": (
                TagSerializer,
                {
                    "many": True,
                },
            ),
            "editor": (PlaylistEditorSerializer,),
        }
