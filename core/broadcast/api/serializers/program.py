# -*- coding: utf-8 -*-
from rest_framework import serializers

from tagging.api.serializers import TagSerializer
from broadcast.api.serializers import EditorSerializer
from broadcast.models import Emission


class ProgramEmissionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:broadcast:emission-detail",
        lookup_field="uid",
    )

    playlist_uid = serializers.CharField(
        source="playlist.uid",
    )
    name = serializers.CharField()
    # series = serializers.CharField(
    #     source="playlist.series",
    #     allow_null=True,
    # )
    series = serializers.DictField(
        source="playlist.series_dict",
        allow_null=True,
    )
    editor = EditorSerializer(
        source="playlist.editor",
    )
    tags = TagSerializer(
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
            "editor",
            "tags",
            "duration",
            "time_start",
            "time_end",
        ]


class ProgramSerializer(serializers.Serializer):
    time_from = serializers.DateTimeField()
    time_until = serializers.DateTimeField()
    emissions = ProgramEmissionSerializer(
        many=True,
    )
