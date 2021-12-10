from django.core.exceptions import FieldError
from django.conf import settings
from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from catalog.api import serializers
from catalog.models import Artist
from tagging import utils as tagging_utils


ARTIST_MIN_NUM_MEDIA = getattr(settings, "CATALOG_ARTIST_MIN_NUM_MEDIA", 1)


def get_search_qs(qs, q):
    qs = qs.filter(Q(name__icontains=q))
    return qs


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

        if q := self.request.GET.get("q", None):
            qs = get_search_qs(qs, q)

        # NOTE: make dynamic...
        qs = qs.filter(num_media__gte=ARTIST_MIN_NUM_MEDIA)
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

    @action(url_path="tags", detail=False, methods=["get"])
    # pylint: disable=unused-argument
    def get_tags(self, request, **kwargs):
        qs = self.get_queryset()
        tags = tagging_utils.get_usage_for_qs(qs)

        tags = tags.exclude(
            type="descriptive",
        )

        try:
            tags = tags.order_by("-num_times")
        except FieldError:
            pass

        # mood_tags = sorted(tags.filter(type="mood")[:6], key=lambda x: x.name)
        mood_tags = []
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
