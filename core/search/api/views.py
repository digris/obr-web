from django.db.models import Q
from rest_framework import mixins, viewsets

from catalog.models import Media
from .serializers import SearchMediaResultSerializer


class GlobalMediaSearchView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = SearchMediaResultSerializer

    def get_queryset(self, **kwargs):
        q = self.request.GET.get("q", "")
        qs = Media.objects.prefetch_related(
            "artists",
            "releases",
            "releases__images",
        )

        qs = qs.filter(
            Q(name__icontains=q)
            | Q(artists__name__icontains=q)
            | Q(releases__name__icontains=q)
        ).distinct()

        return qs