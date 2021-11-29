# -*- coding: utf-8 -*-
from django.core.exceptions import FieldError
from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from catalog.api import serializers
from catalog.models import Playlist
from tagging import utils as tagging_utils

MEDIA_MIN_DURATION = 12


class PlaylistFilter(filters.FilterSet):
    obj_key = filters.CharFilter(method="obj_key_filter")
    user_rating = filters.NumberFilter(method="user_rating_filter")

    class Meta:
        model = Playlist
        fields = ["obj_key"]

    @staticmethod
    def get_obj_query(obj_ct, obj_uid):
        # Not so nice... striping fixed "catalog."
        app, model = obj_ct.split(".")

        if model == "media":
            return {
                "media__uid": obj_uid,
            }

        if model == "editor":
            return {
                f"{model}__uid": obj_uid,
            }

        return {
            f"{model}s__uid": obj_uid,
        }

    # pylint: disable=unused-argument
    def obj_key_filter(self, queryset, name, value):
        obj_ct, obj_uid = value.split(":")
        query = self.get_obj_query(obj_ct, obj_uid)
        qs = queryset.filter(**query)
        return qs

    # # pylint: disable=unused-argument
    # def obj_key_filter(self, queryset, name, value):
    #     obj_ct, obj_uid = value.split(":")
    #     # TODO: implement in a better / real way
    #     ct = obj_ct[8:]
    #     if ct != "media":
    #         ct = ct + "s"
    #     query = {
    #         f"{ct}__uid": obj_uid,
    #     }
    #     return queryset.filter(**query)

    # pylint: disable=unused-argument
    def user_rating_filter(self, queryset, name, value):
        query = {
            "user_rating__gte": value,
        }
        return queryset.filter(**query)


def get_search_qs(qs, q):
    qs = qs.filter(Q(name__icontains=q) | Q(series__name__icontains=q))
    return qs


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
                "emissions__time_start",
                filter=Q(emissions__time_start__lte=Now()),
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
        elif hasattr(self.request, "user_identity"):
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value",
                    filter=Q(votes__user_identity=self.request.user_identity),
                ),
            )

        qs = qs.filter(latest_emission__lte=Now())

        # tag handling (filter seems to not support `tags[]=***`)
        tag_uids = self.request.GET.getlist(
            "tags[]", self.request.GET.getlist("tags", [])
        )

        if q := self.request.GET.get("q", None):
            qs = get_search_qs(qs, q)

        for uid in tag_uids:
            qs = qs.filter(tags__uid=uid)

        qs = qs.order_by("-latest_emission")
        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:  # pragma: no cover
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj

    @action(url_path="tags", detail=False, methods=["get"])
    # pylint: disable=unused-argument
    def get_tags(self, request, **kwargs):
        qs_filter = PlaylistFilter(request.GET, queryset=self.get_queryset())
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
