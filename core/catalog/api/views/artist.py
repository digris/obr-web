# -*- coding: utf-8 -*-
from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from catalog.api import serializers
from catalog.models import Artist

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
        qs = qs.filter(num_media__gt=0)
        qs = qs.order_by("-created")

        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:  # pragma: no cover
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

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
