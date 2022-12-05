from rest_framework import mixins, viewsets

from ..models import Category
from . import serializers


class CategoryViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        # qs = self.queryset.prefetch_related(
        #     'translations',
        # )
        return self.queryset
