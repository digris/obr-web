from datetime import timedelta

from django.db.models import Q

from catalog.models import Media
from rest_framework import mixins, viewsets

from .serializers import SearchMediaResultSerializer

MEDIA_MIN_DURATION = 12


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

        qs = qs.exclude(kind=Media.Kind.JINGLE)

        qs = qs.filter(duration__gt=timedelta(seconds=MEDIA_MIN_DURATION))

        qs = qs.filter(
            Q(name__unaccent__icontains=q)
            | Q(artists__name__unaccent__icontains=q)
            | Q(releases__name__unaccent__icontains=q),
        ).distinct()

        return qs
