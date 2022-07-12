import logging

from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ParseError

from broadcast.api import serializers
from broadcast.models import Emission
from stats.models import Emission as ArchivedEmission

logger = logging.getLogger(__name__)

PROGRAM_MAX_EMISSIONS = 100


class EmissionViewSet(
    # mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Emission.objects.all()
    serializer_class = serializers.EmissionSerializer
    lookup_field = "uid"

    def get_object(self):
        try:
            obj_uid = self.kwargs["uid"]
            assert len(obj_uid) == 8
        except AssertionError as e:
            raise ParseError(f"Invalid UID: {self.kwargs['uid']}") from e

        if obj := Emission.objects.filter(uid=obj_uid).first():
            return obj

        return get_object_or_404(ArchivedEmission, uid=obj_uid)
