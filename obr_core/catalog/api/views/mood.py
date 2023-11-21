from django.shortcuts import get_object_or_404

from catalog.api import serializers
from catalog.models import Mood
from rating.queries import annotate_qs_width_user_rating
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

MEDIA_MIN_DURATION = 12


class MoodViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Mood.objects.all()
    serializer_class = serializers.MoodSerializer
    lookup_field = "uid"

    def get_queryset(self):
        qs = self.queryset
        qs = annotate_qs_width_user_rating(qs, self.request)
        qs = qs.order_by("user_rating", "name")
        return qs

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:  # pragma: no cover
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj
