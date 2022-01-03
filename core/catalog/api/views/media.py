from datetime import timedelta

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
from catalog.models import Media, Playlist
from tagging import utils as tagging_utils

MEDIA_MIN_DURATION = 12


class MediaFilter(filters.FilterSet):
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


def get_search_qs(qs, q):
    qs = qs.filter(
        Q(name__icontains=q)
        | Q(artists__name__icontains=q)
        | Q(releases__name__icontains=q)
    )
    return qs


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

    def get_queryset(self, include_upcoming=False):

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
                    # filter=Q(airplays__time_start__lte=Now()),
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

        # qs = qs.filter(latest_airplay__lte=Now())
        if not include_upcoming:
            qs = qs.filter(latest_airplay__lte=Now())

        # tag handling (filter seems to not support `tags[]=***`)
        tag_uids = self.request.GET.getlist(
            "tags[]", self.request.GET.getlist("tags", [])
        )

        if q := self.request.GET.get("q", None):
            qs = get_search_qs(qs, q)

        for uid in tag_uids:
            qs = qs.filter(tags__uid=uid)

        qs = qs.filter(
            duration__gt=timedelta(seconds=MEDIA_MIN_DURATION),
        )

        qs = qs.order_by("-latest_airplay")

        return qs

    def get_object(self):

        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

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

        qs = self.filter_queryset(self.get_queryset(include_upcoming=True))

        print('list_for_playlist', qs.count())
        playlist = Playlist.objects.get(uid=uid)
        qs_media_ids = qs.values_list("id", flat=True)
        media_ids = []
        for playlist_media in playlist.playlist_media.all():
        # for playlist_media in playlist.airplayed_playlist_media:
            if playlist_media.media.id not in qs_media_ids:
                continue
            media_ids.append(playlist_media.media.id)

        # pylint: disable=consider-using-dict-comprehension
        d = {obj.id: obj for obj in qs}
        media = [d[index] for index in media_ids]

        serializer = self.get_serializer(media, many=True)
        data = {
            "results": serializer.data,
        }
        return Response(data)

    # def list_for_playlist(self, request, uid, *args, **kwargs):
    #     playlist = Playlist.objects.get(uid=uid)
    #     media = []
    #     for playlist_media in playlist.playlist_media.all():
    #         media.append(playlist_media.media)
    #     serializer = self.get_serializer(media, many=True)
    #     data = {
    #         "results": serializer.data,
    #     }
    #     return Response(data)

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
