# -*- coding: utf-8 -*-
import logging

from django.core.exceptions import FieldError
from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from tagging import utils as tagging_utils
from . import serializers
from ..models import Mood, Media, Artist, Release, Playlist

logger = logging.getLogger(__name__)


class MoodViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Mood.objects.all().order_by("name")
    serializer_class = serializers.MoodSerializer
    lookup_field = "uid"

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj


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
            "votes",
            "votes__user",
        )
        qs = qs.annotate(
            num_media=Count(
                "media",
                filter=Q(media__airplays__time_start__lte=Now()),
                distinct=True,
            )
        )

        # annotate with request user's rating
        if self.request.user.is_authenticated:
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value", filter=Q(votes__user=self.request.user)
                ),
            )
        # annotate with anonymous user 'identity'
        else:
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value",
                    filter=Q(votes__user_identity=self.request.user_identity),
                ),
            )

        # NOTE: make dynamic...
        qs = qs.filter(num_media__gt=0)
        qs = qs.order_by("-created")

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
    obj_key = filters.CharFilter(method="obj_key_filter")
    user_rating = filters.NumberFilter(method="user_rating_filter")

    class Meta:
        model = Media
        fields = ["obj_key"]

    # pylint: disable=unused-argument
    def obj_key_filter(self, queryset, name, value):
        obj_ct, obj_uid = value.split(":")
        query = {
            f"{obj_ct[8:]}s__uid": obj_uid,
        }
        qs = queryset.filter(**query)
        return qs

    # pylint: disable=unused-argument
    def user_rating_filter(self, queryset, name, value):
        query = {
            "user_rating__gte": value,
        }
        return queryset.filter(**query)


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
    """

    queryset = Media.objects.all()
    serializer_class = serializers.MediaSerializer
    lookup_field = "uid"

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MediaFilter

    def get_queryset(self):

        qs = self.queryset
        qs = qs.prefetch_related(
            "artists",
            "media_artist",
            "media_artist__artist",
            "releases",
            "releases__images",
            "releases__media",
            "votes",
            "votes__user",
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

        # annotate with request user's rating
        if self.request.user.is_authenticated:
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value", filter=Q(votes__user=self.request.user)
                ),
            )
        # annotate with anonymous user 'identity'
        else:
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value",
                    filter=Q(votes__user_identity=self.request.user_identity),
                ),
            )

        qs = qs.filter(latest_airplay__lte=Now())

        # tag handling (filter seems to not support `tags[]=***`)
        tag_uids = self.request.GET.getlist(
            "tags[]", self.request.GET.getlist("tags", [])
        )

        for uid in tag_uids:
            qs = qs.filter(tags__uid=uid)

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

    def list(self, request, *args, **kwargs):
        # TODO: implement "playlist case"
        try:
            obj_ct, obj_uid = request.GET.get("obj_key", "").split(":")
            if obj_ct == "catalog.playlist":
                return self.list_for_playlist(request, obj_uid, *args, **kwargs)
        except ValueError:
            pass
        return super().list(request, *args, **kwargs)

    def list_for_playlist(self, request, uid, *args, **kwargs):
        playlist = Playlist.objects.get(uid=uid)
        media = []
        for playlist_media in playlist.playlist_media.all():
            media.append(playlist_media.media)
        serializer = self.get_serializer(media, many=True)
        data = {
            "results": serializer.data,
        }
        return Response(data)

    @action(url_path="tags", detail=False, methods=["get"])
    # pylint: disable=unused-argument
    def get_tags(self, request, **kwargs):
        qs_filter = MediaFilter(request.GET, queryset=self.get_queryset())
        qs = qs_filter.qs
        tags = tagging_utils.get_usage_for_qs(qs)

        tags = tags.exclude(
            type="descriptive",
        )

        try:
            tags = tags.order_by("-num_times")
        except FieldError:
            pass

        mood_tags = sorted(tags.filter(type="mood")[:6], key=lambda x: x.name)
        other_tags = sorted(tags.exclude(type="mood")[:12], key=lambda x: x.name)

        data = []
        # for t in sorted(tags[:30], key=lambda x: x.name):
        for t in mood_tags + other_tags:
            data.append(
                {
                    "uid": t.uid,
                    "type": t.type,
                    "name": t.name,
                    "count": t.num_times,
                }
            )

        return Response(data)


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


class PlaylistFilter(filters.FilterSet):
    obj_key = filters.CharFilter(method="obj_key_filter")
    user_rating = filters.NumberFilter(method="user_rating_filter")

    class Meta:
        model = Playlist
        fields = ["obj_key"]

    # pylint: disable=unused-argument
    def obj_key_filter(self, queryset, name, value):
        obj_ct, obj_uid = value.split(":")
        # TODO: implement in a better / real way
        ct = obj_ct[8:]
        if ct != "media":
            ct = ct + "s"
        query = {
            f"{ct}__uid": obj_uid,
        }
        return queryset.filter(**query)

    # pylint: disable=unused-argument
    def user_rating_filter(self, queryset, name, value):
        query = {
            "user_rating__gte": value,
        }
        return queryset.filter(**query)


class PlaylistViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Playlist.objects.all().order_by("name")
    serializer_class = serializers.PlaylistSerializer
    lookup_field = "uid"

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PlaylistFilter

    def get_queryset(self):
        qs = self.queryset.prefetch_related(
            "media",
            "emissions",
            "images",
            "playlist_media",
            "playlist_media__media",
            "series",
        )
        qs = qs.annotate(
            num_media=Count("media"),
            latest_emission=Max(
                "emissions__time_end",
                filter=Q(emissions__time_end__lte=Now()),
            ),
            num_emissions=Count(
                "emissions",
                filter=Q(emissions__time_end__lte=Now()),
            ),
        )

        # annotate with request user's rating
        if self.request.user.is_authenticated:
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value", filter=Q(votes__user=self.request.user)
                ),
            )
        # annotate with anonymous user 'identity'
        else:
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value",
                    filter=Q(votes__user_identity=self.request.user_identity),
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
