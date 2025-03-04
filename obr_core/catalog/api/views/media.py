from datetime import timedelta

from django.core.exceptions import FieldError
from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404

from catalog.api import serializers
from catalog.models import Media, Playlist
from django_filters import rest_framework as filters
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from tagging import utils as tagging_utils

MEDIA_MIN_DURATION = 12
DEFAULT_ORDER_BY = "-latest_airplay"
NUM_MOOD_TAGS = 14
NUM_OTHER_TAGS = 28


class MediaFilter(
    filters.FilterSet,
):
    obj_key = filters.CharFilter(method="obj_key_filter")
    user_rating = filters.NumberFilter(method="user_rating_filter")

    class Meta:
        model = Media
        fields = ["obj_key"]

    @staticmethod
    def get_obj_query(obj_ct, obj_uid):
        # Not so nice... striping fixed "catalog."
        ct = obj_ct[8:]

        if ct == "media":
            return {
                "uid": obj_uid,
            }

        if ct == "mood":
            return {}

        return {
            f"{ct}s__uid": obj_uid,
        }

    # pylint: disable=unused-argument
    def obj_key_filter(self, queryset, name, value):
        obj_ct, obj_uid = value.split(":")
        query = self.get_obj_query(obj_ct, obj_uid)
        qs = queryset.filter(**query)
        return qs

    # pylint: disable=unused-argument
    def user_rating_filter(self, queryset, name, value):
        query = {
            "user_rating__gte": value,
        }
        return queryset.filter(**query)

    def filter_queryset(self, queryset, *args, **kwargs):
        qs = super().filter_queryset(queryset)

        try:
            order_by = self.request.GET.get("ordering", DEFAULT_ORDER_BY)
            order_by = order_by or DEFAULT_ORDER_BY
        except AttributeError:
            order_by = DEFAULT_ORDER_BY

        try:
            if order_by == "time_rated":
                if self.request.user.is_authenticated:
                    qs = qs.annotate(
                        user_rating_time_rated=Max(
                            "votes__created",
                            filter=Q(
                                votes__user=self.request.user,
                            ),
                        ),
                    )
                    return qs.order_by("-user_rating_time_rated")

                return qs.order_by(DEFAULT_ORDER_BY)

        except AttributeError:
            pass

        qs = qs.order_by(order_by)

        return qs


def get_search_qs(qs, q):
    qs = qs.filter(
        Q(name__icontains=q)
        | Q(artists__name__icontains=q)
        | Q(releases__name__icontains=q),
    )
    return qs


class MediaViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Media endpoint.
    """

    queryset = Media.objects.all()
    serializer_class = serializers.MediaSerializer
    lookup_field = "uid"

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MediaFilter

    def get_queryset(self, **kwargs):
        include_upcoming = kwargs.get("include_upcoming", False)

        qs = self.queryset
        qs = qs.prefetch_related(
            "artists",
            "media_artist",
            "media_artist__artist",
            "releases",
            "releases__images",
            "releases__media",
            "releases__label",
            "votes",
            "votes__user",
        )

        if include_upcoming:
            qs = qs.annotate(
                latest_airplay=Max(
                    "airplays__time_start",
                ),
                num_airplays=Count(
                    "airplays",
                ),
            )
        else:
            qs = qs.annotate(
                latest_airplay=Max(
                    "airplays__time_start",
                    filter=Q(
                        airplays__time_start__lte=Now(),
                    ),  # NOTE: check for implications
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
                    "votes__value",
                    filter=Q(votes__user=self.request.user),
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

        if not include_upcoming:
            qs = qs.filter(latest_airplay__lte=Now())

        # tag handling (filter seems to not support `tags[]=***`)
        tag_uids = self.request.GET.getlist(
            "tags[]",
            self.request.GET.getlist("tags", []),
        )

        if q := self.request.GET.get("q", None):
            qs = get_search_qs(qs, q)

        for uid in tag_uids:
            qs = qs.filter(tags__uid=uid)

        qs = qs.filter(
            duration__gt=timedelta(seconds=MEDIA_MIN_DURATION),
        )

        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        obj = get_object_or_404(self.queryset, uid=obj_uid)

        return obj

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="obj_key",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                description="""Filter media belonging to a related object.
                               format: `<ct>:<uid>`""",
                examples=[
                    OpenApiExample(
                        'Get tracks for artist "Johnny Cash"',
                        value="catalog.artist:B38B2649",
                    ),
                    OpenApiExample(
                        'Get tracks for mood "Good Vibes"',
                        value="catalog.mood:53017FE1",
                    ),
                    OpenApiExample(
                        'Get tracks for playlist "DEV - FADE / CUE"',
                        value="catalog.playlist:80FB3498",
                    ),
                ],
            ),
            OpenApiParameter(
                name="expand",
                location=OpenApiParameter.QUERY,
                enum=["image", "tags", "identifiers"],
                many=True,
                description="""Expand nested resources, multiple values possible.""",
                examples=[
                    OpenApiExample(
                        "Expand primary image & tags",
                        value="image,tags",
                    ),
                ],
            ),
            OpenApiParameter(
                name="user_rating",
                type=OpenApiTypes.STR,
                enum=[-1, 1],
                description="""Limit results based on current user's rating \u2764""",
                examples=[
                    OpenApiExample(
                        "User's favorites",
                        value=1,
                    ),
                    OpenApiExample(
                        "User's dislikes",
                        value=-1,
                    ),
                ],
            ),
        ],
        responses={
            200: serializers.MediaSerializer(
                many=True,
                expand=[
                    "image",
                    "tags",
                    "identifiers",
                ],
            ),
        },
    )
    def list(self, request, *args, **kwargs):
        # TODO: implement "playlist case"
        try:
            obj_ct, obj_uid = request.GET.get("obj_key", "").split(":")
            if obj_ct == "catalog.playlist":
                return self.list_for_playlist(request, obj_uid, *args, **kwargs)
        except ValueError:
            pass
        return super().list(request, *args, **kwargs)

    # pylint: disable=too-many-locals
    def list_for_playlist(self, request, uid, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset(include_upcoming=True))

        playlist = Playlist.objects.get(uid=uid)
        qs_media_ids = qs.values_list("id", flat=True)
        media_ids = []
        cue_fade = []
        for playlist_media in playlist.playlist_media.all():
            if playlist_media.media.id not in qs_media_ids:
                continue
            media_ids.append(playlist_media.media.id)
            cue_fade.append(
                {
                    "cue_in": playlist_media.cue_in,
                    "cue_out": playlist_media.cue_out,
                    "fade_in": playlist_media.fade_in,
                    "fade_out": playlist_media.fade_out,
                },
            )

        # pylint: disable=consider-using-dict-comprehension
        d = {obj.id: obj for obj in qs}
        media = [d[index] for index in media_ids]

        for index, m in enumerate(media):
            m.cue_in = cue_fade[index]["cue_in"] / 1000.0
            m.cue_out = cue_fade[index]["cue_out"] / 1000.0
            m.fade_in = cue_fade[index]["fade_in"] / 1000.0
            m.fade_out = cue_fade[index]["fade_out"] / 1000.0

        page = self.paginate_queryset(media)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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

        try:  # NOQA: SIM105
            tags = tags.order_by("-num_times")
        except FieldError:
            pass

        mood_tags = sorted(
            tags.filter(type="mood")[:NUM_MOOD_TAGS],
            key=lambda x: x.name,
        )
        other_tags = sorted(
            tags.exclude(type="mood")[:NUM_OTHER_TAGS],
            key=lambda x: x.name,
        )

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
