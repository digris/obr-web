import logging

from django.db.models import Count
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from broadcast.api import serializers
from broadcast.models import Editor

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100


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
            )
        )
        qs = qs.filter(
            num_playlists__gte=5,
        )
        qs = qs.order_by(
            Lower("display_name"),
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
