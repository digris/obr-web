# -*- coding: utf-8 -*-
import logging
import time

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count, Max, Q
from django.db.models.functions import Now

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.compat import coreapi
from rest_framework.compat import coreschema
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters

from ..models import Media, Artist, Release, Playlist
from . import serializers


logger = logging.getLogger(__name__)


class ArtistViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Artist endpoint.
    """

    queryset = Artist.objects.all().order_by("name")
    serializer_class = serializers.ArtistSerializer
    lookup_field = "uid"

    def get_queryset(self):
        # time.sleep(2)
        qs = self.queryset
        qs = qs.prefetch_related(
            "media",
            "images",
        )
        qs = qs.annotate(num_media=Count("media"))
        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj


class MediaFilter(filters.FilterSet):
    playlist = filters.CharFilter(method="playlist_filter")
    artist = filters.CharFilter(method="artist_filter")

    class Meta:
        model = Media
        fields = ["playlist"]

    def playlist_filter(self, queryset, name, value):
        return queryset.filter(playlists__uid=value)

    def artist_filter(self, queryset, name, value):
        return queryset.filter(artists__uid=value)


class MediaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Media endpoint.

    retrieve:
    Returns a media instance.

    list:
    Returns all a list of media...

    artists:
    Returns appearing artists.

    """

    queryset = Media.objects.all()
    serializer_class = serializers.MediaSerializer
    lookup_field = "uid"
    # permission_classes = (IsAuthenticated,)
    # filter_backends = [
    #     ControllerListFilter,
    # ]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MediaFilter

    def get_queryset(self):

        qs = self.queryset
        qs = qs.prefetch_related(
            "artists",
            "media_artist",
            "media_artist__artist",
        )

        qs = qs.annotate(
            latest_airplay=Max(
                "airplays__time_start",
                filter=Q(airplays__time_start__lte=Now()),
            ),
            num_airplays=Count(
                "airplays",
                filter=Q(airplays__time_start__lte=Now()),
            ),
        )

        qs = qs.filter(latest_airplay__lte=Now())

        qs = qs.order_by("-latest_airplay")

        return qs

    def get_object(self):

        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj


class ReleaseViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Release.objects.all().order_by("-created")
    serializer_class = serializers.ReleaseSerializer
    lookup_field = "uid"

    def get_queryset(self):
        qs = self.queryset.prefetch_related("media")
        return qs

    def get_object(self):

        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj


class PlaylistViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Playlist.objects.all().order_by("name")
    serializer_class = serializers.PlaylistSerializer
    lookup_field = "uid"

    def get_queryset(self):
        qs = self.queryset.prefetch_related(
            "media",
            "emissions",
            "images",
            "playlist_media",
            "playlist_media__media",
        )
        qs = qs.annotate(
            num_media=Count("media"),
            latest_emission=Max(
                "emissions__time_start",
                filter=Q(emissions__time_start__lte=Now()),
            ),
            num_emissions=Count(
                "emissions",
                filter=Q(emissions__time_start__lte=Now()),
            ),
        )

        qs = qs.filter(latest_emission__lte=Now())

        qs = qs.order_by("-latest_emission")
        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj
