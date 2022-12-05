import logging

from django.db.models import Count, Max, Q
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404

from broadcast.api import serializers
from broadcast.models import Editor
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rating.queries import annotate_qs_width_user_rating
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100

# @extend_schema_view(
#     retrieve=extend_schema(description='text')
# )
@extend_schema(
    parameters=[
        OpenApiParameter(
            name="expand",
            location=OpenApiParameter.QUERY,
            enum=["tags", "identifiers"],
            many=True,
        ),
    ],
)
class EditorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Editor.objects.all()
    serializer_class = serializers.EditorSerializer
    lookup_field = "uid"

    def get_queryset(self):
        qs = self.queryset.select_related("user")
        qs = qs.prefetch_related(
            "playlists",
            "images",
        )
        qs = qs.annotate(
            num_playlists=Count(
                "playlists",
            ),
            latest_emission=Max(
                "playlists__emissions__time_start",
                filter=Q(
                    playlists__emissions__time_start__lte=Now(),
                ),
            ),
        )
        qs = annotate_qs_width_user_rating(qs, self.request)
        qs = qs.order_by("-latest_emission")
        return qs

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        qs = qs.filter(
            num_playlists__gte=1,
        )
        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj
