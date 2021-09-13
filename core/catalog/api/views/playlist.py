# -*- coding: utf-8 -*-
from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from catalog.api import serializers
from catalog.models import Playlist

MEDIA_MIN_DURATION = 12


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
