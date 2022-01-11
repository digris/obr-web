from rest_framework import serializers

from ..models import Vote, VoteScope


# SITE_URL = getattr(settings, 'SITE_URL')


class VoteSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(
        min_value=-1,
        max_value=1,
        allow_null=True,
    )
    scope = serializers.ChoiceField(
        choices=VoteScope.choices,
        write_only=True,
        required=False,
    )
    comment = serializers.CharField(
        write_only=True,
        required=False,
    )

    class Meta:
        model = Vote
        depth = 1
        fields = [
            "key",
            "value",
            "scope",
            "comment",
            "updated",
        ]
