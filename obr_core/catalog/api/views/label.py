from django.shortcuts import get_object_or_404

from catalog.api import serializers
from catalog.models import Label
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError


class LabelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Label.objects.all().order_by("-created")
    serializer_class = serializers.LabelSerializer
    lookup_field = "uid"

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        obj = get_object_or_404(self.get_queryset(), uid=obj_uid)

        return obj
