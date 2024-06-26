from api_extra.serializers import CTUIDModelSerializer
from rest_framework import serializers

from ..models import Vote, VoteScope, VoteSource


class VoteSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    key = serializers.CharField()
    value = serializers.IntegerField(
        min_value=-1,
        max_value=1,
        read_only=True,
    )
    source = serializers.ChoiceField(
        choices=VoteSource.choices,
        read_only=True,
    )
    scope = serializers.ChoiceField(
        choices=VoteScope.choices,
        read_only=True,
    )
    comment = serializers.CharField(
        read_only=True,
    )
    is_anonymous = serializers.BooleanField(
        read_only=True,
    )
    totals = serializers.JSONField(
        read_only=True,
        source="get_totals",
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Vote
        depth = 1
        fields = CTUIDModelSerializer.Meta.fields + [
            "key",
            "value",
            "source",
            "scope",
            "comment",
            "updated",
            "is_anonymous",
            "totals",
        ]


class VoteWriteSerializer(
    serializers.ModelSerializer,
):
    key = serializers.CharField()
    value = serializers.IntegerField(
        min_value=-1,
        max_value=1,
        allow_null=True,
    )
    source = serializers.ChoiceField(
        choices=VoteSource.choices,
        write_only=True,
        required=False,
        allow_null=True,
    )
    scope = serializers.ChoiceField(
        choices=VoteScope.choices,
        write_only=True,
        required=False,
        allow_null=True,
    )
    comment = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = Vote
        depth = 1
        fields = [
            "key",
            "value",
            "source",
            "scope",
            "comment",
            "updated",
        ]
