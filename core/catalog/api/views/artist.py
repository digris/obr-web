# -*- coding: utf-8 -*-

from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from catalog.api import serializers
from catalog.models import Media, Artist

MEDIA_MIN_DURATION = 12


class ArtistViewSet(
    FlexFieldsMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Artist endpoint.
    """

    queryset = Artist.objects.all().order_by("name")
    permit_list_expands = [
        "tags",
    ]
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
        elif hasattr(self.request, "user_identity"):
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value",
                    filter=Q(votes__user_identity=self.request.user_identity),
                ),
            )

        # NOTE: make dynamic...
        # qs = qs.filter(num_media__gt=0)
        qs = qs.order_by("-created")

        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError:  # pragma: no cover
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}")

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj

    @extend_schema(
        parameters=[
            OpenApiParameter("expand"),
        ],
        responses={
            200: serializers.ArtistSerializer(
                expand=[
                    "tags",
                ],
                fields=[
                    "uid",
                    "tags",
                ],
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # def get_serializer(self, *args, **kwargs):
    #     serializer = super().get_serializer(*args, **kwargs)
    #     return serializer


# class MediaFilter(filters.FilterSet):
#     obj_key = filters.CharFilter(
#         method="obj_key_filter",
#     )
#     user_rating = filters.NumberFilter(
#         method="user_rating_filter",
#     )
#
#     class Meta:
#         model = Media
#         fields = ["obj_key"]
#
#     @staticmethod
#     def get_obj_query(obj_ct, obj_uid):
#
#         # Not so nice... striping fixed "catalog."
#         ct = obj_ct[8:]
#
#         if ct == "media":
#             return {
#                 "uid": obj_uid,
#             }
#
#         if ct == "mood":
#             return {}
#
#         return {
#             f"{ct}s__uid": obj_uid,
#         }
#
#     # pylint: disable=unused-argument
#     def obj_key_filter(self, queryset, name, value):
#         obj_ct, obj_uid = value.split(":")
#         # query = {
#         #     f"{obj_ct[8:]}s__uid": obj_uid,
#         # }
#         query = self.get_obj_query(obj_ct, obj_uid)
#         qs = queryset.filter(**query)
#         return qs
#
#     # pylint: disable=unused-argument
#     def user_rating_filter(self, queryset, name, value):
#         query = {
#             "user_rating__gte": value,
#         }
#         return queryset.filter(**query)
