# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_framework import serializers

from ..models import Artist, Media


SITE_URL = getattr(settings, "SITE_URL")

logger = logging.getLogger(__name__)


class DurationInSecondsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if not instance:
            return None

        return instance.seconds


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="api:catalog:artist-detail",
        lookup_field="uid",
    )

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

    class Meta:
        model = Media
        fields = [
            "url",
            "ct",
            # "uuid",
            "uid",
            "name",
            "artist_display",
            "duration",
        ]
