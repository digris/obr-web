from datetime import timedelta

from django.conf import settings
from django.core.exceptions import FieldError
from django.db.models import Count, Max, Q, Sum
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404

from catalog.api import serializers
from catalog.models import Artist
from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from tagging import utils as tagging_utils

MEDIA_MIN_DURATION = 12
# DEFAULT_ORDER_BY = "-created"
DEFAULT_ORDER_BY = "-latest_airplay"
ARTIST_MIN_NUM_MEDIA = getattr(settings, "CATALOG_ARTIST_MIN_NUM_MEDIA", 1)


class ArtistFilter(filters.FilterSet):
    user_rating = filters.NumberFilter(
        method="user_rating_filter",
    )

    class Meta:
        model = Artist
        fields = []

    # pylint: disable=unused-argument
    def user_rating_filter(self, queryset, name, value):
        query = {
            "user_rating__gte": value,
        }
        return queryset.filter(**query)

    def filter_queryset(self, queryset, *args, **kwargs):
        qs = super().filter_queryset(queryset)
        try:
            ordering = self.request.GET.get("ordering", DEFAULT_ORDER_BY)
            if ordering == "time_rated" and self.request.user.is_authenticated:
                qs = qs.annotate(
                    user_rating_time_rated=Max(
                        "votes__created",
                        filter=Q(
                            votes__user=self.request.user,
                        ),
                    ),
                )
                qs = qs.order_by("-user_rating_time_rated")
                return qs

        except AttributeError:
            pass

        qs = qs.order_by(DEFAULT_ORDER_BY)

        return qs


def get_search_qs(qs, q):
    qs = qs.filter(name__unaccent__icontains=q)
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

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArtistFilter

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
                filter=Q(
                    media__airplays__time_start__lte=Now(),
                )
                & Q(
                    media__duration__gt=timedelta(seconds=MEDIA_MIN_DURATION),
                ),
                distinct=True,
            ),
            media_total_duration=Sum(
                "media__duration",
                filter=Q(
                    media__airplays__time_start__lte=Now(),
                )
                & Q(
                    media__duration__gt=timedelta(seconds=MEDIA_MIN_DURATION),
                ),
                distinct=True,
            ),
            latest_airplay=Max(
                "media__airplays__time_start",
                filter=Q(
                    media__airplays__time_start__lte=Now(),
                )
                & Q(
                    media__duration__gt=timedelta(seconds=MEDIA_MIN_DURATION),
                ),
            ),
        )

        # annotate with request user's rating
        if self.request.user.is_authenticated:
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value",
                    filter=Q(
                        votes__user=self.request.user,
                    ),
                ),
            )
        # annotate with anonymous user 'identity'
        elif hasattr(self.request, "user_identity"):
            qs = qs.annotate(
                user_rating=Max(
                    "votes__value",
                    filter=Q(
                        votes__user_identity=self.request.user_identity,
                    ),
                ),
            )

        if q := self.request.GET.get("q", None):
            qs = get_search_qs(qs, q)
            # qs = qs.filter(name__unaccent__icontains="castelle")

        # tag handling (filter seems to not support `tags[]=***`)
        tag_uids = self.request.GET.getlist(
            "tags[]",
            self.request.GET.getlist("tags", []),
        )

        for uid in tag_uids:
            qs = qs.filter(tags__uid=uid)

        # NOTE: make dynamic...
        qs = qs.filter(
            num_media__gte=ARTIST_MIN_NUM_MEDIA,
        )

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

        try:  # NOQA: SIM105
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
                },
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
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
