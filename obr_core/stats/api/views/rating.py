from django_filters import rest_framework as filters
from rating.api.serializers import VoteSerializer as RatingVoteSerializer
from rating.models import Vote
from rest_framework import mixins, serializers, viewsets
from stats.api import permissions


class VoteSerializer(
    RatingVoteSerializer,
):
    user = serializers.EmailField(
        source="user.email",
        allow_null=True,
    )

    class Meta(RatingVoteSerializer.Meta):
        model = Vote
        ref_name = "StatsVote"
        fields = RatingVoteSerializer.Meta.fields + [
            "user",
        ]


class RatingFilter(
    filters.FilterSet,
):
    for_year = filters.NumberFilter(
        field_name="updated",
        lookup_expr="year",
    )
    time_from = filters.DateTimeFilter(
        field_name="updated",
        lookup_expr="gt",
    )

    class Meta:
        model = Vote
        fields = [
            "source",
            "scope",
            "value",
        ]


class RatingViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    permission_classes = [
        permissions.ViewPermission,
    ]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RatingFilter
