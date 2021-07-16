# -*- coding: utf-8 -*-
import logging

from django.core.exceptions import FieldError
from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
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
    # playlist = filters.CharFilter(method="playlist_filter")
    # artist = filters.CharFilter(method="artist_filter")
    obj_key = filters.CharFilter(method="obj_key_filter")
    # tags = filters.CharFilter(method="tag_filter", field_name="tags[]")
    user_rating = filters.NumberFilter(method="user_rating_filter")

    class Meta:
        model = Media
        fields = ["obj_key"]

    # # pylint: disable=unused-argument
    # def playlist_filter(self, queryset, name, value):
    #     return queryset.filter(playlists__uid=value)
    #
    # # pylint: disable=unused-argument
    # def artist_filter(self, queryset, name, value):
    #     return queryset.filter(artists__uid=value)

    # pylint: disable=unused-argument
    def obj_key_filter(self, queryset, name, value):
        obj_ct, obj_uid = value.split(":")
        query = {
            f"{obj_ct[8:]}s__uid": obj_uid,
        }
        return queryset.filter(**query)

    # # pylint: disable=unused-argument
    # def tag_filter(self, queryset, name, value):
    #     print("**", name, value)
    #     return queryset

    # pylint: disable=unused-argument
    def user_rating_filter(self, queryset, name, value):
        query = {
            f"user_rating__gte": value,
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

        # qs = qs.filter(user_rating__gte=1)

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

    @action(url_path="tags", detail=False, methods=["get"])
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
