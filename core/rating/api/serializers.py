from rest_framework import serializers

from ..models import Vote, VoteScope, VoteSource

# SITE_URL = getattr(settings, 'SITE_URL')


class VoteSerializer(serializers.ModelSerializer):
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
