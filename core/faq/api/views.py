from rest_framework import mixins, viewsets
from . import serializers
from ..models import Category


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
