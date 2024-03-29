from api_extra.serializers import CTUIDModelSerializer
from broadcast.models.editor import Editor, EditorImage
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiTypes,
    extend_schema_field,
    extend_schema_serializer,
)
from identifier.api.serializers import IdentifierSerializer
from image.api.serializers import BaseImageSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from rest_framework import serializers
from tagging.api.serializers import TagSerializer


class ImageSerializer(
    BaseImageSerializer,
):
    class Meta(BaseImageSerializer.Meta):
        model = EditorImage
        ref_name = "EditorImage"


@extend_schema_serializer(
    exclude_fields=("single",),  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Example",
            value={
                "url": "/api/v1/broadcast/editors/3144C75B/",
                "ct": "broadcast.editor",
                "uid": "3144C75B",
                "name": "bang Goes",
                "is_active": True,
                "image": {
                    "uid": "60D49C10",
                    "file": "broadcast/editor/234B03E6/60D49C10.jpeg",
                    "path": "ch-openbroadcast-media/broadcast/editor/234B03E6/60D49C10.jpeg",
                    "rgb": [134, 116, 66],
                },
            },
            response_only=True,
        ),
    ],
)
class EditorSerializer(
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
        read_only=True,
    )
    role = serializers.SerializerMethodField()
    num_playlists = serializers.IntegerField(
        read_only=True,
    )
    user_rating = serializers.IntegerField(
        read_only=True,
        allow_null=True,
    )
    image = ImageSerializer(
        read_only=True,
        allow_null=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Editor
        fields = CTUIDModelSerializer.Meta.fields + [
            "url",
            "name",
            "location",
            "description",
            "role",
            "num_playlists",
            "user_rating",
            "image",
            "is_active",
        ]
        expandable_fields = {
            "tags": (
                TagSerializer,
                {
                    "many": True,
                    "required": False,
                    "allow_null": True,
                },
            ),
            "identifiers": (
                IdentifierSerializer,
                {
                    "many": True,
                    "required": False,
                    "allow_null": True,
                },
            ),
        }

    @staticmethod
    @extend_schema_field(OpenApiTypes.STR)
    def get_role(obj):
        return obj.get_role_display()
