from rest_framework import serializers
from sync.update import SYNC_APP_LABELS


class SyncScheduleSerializer(serializers.Serializer):
    num_hours = serializers.IntegerField(
        allow_null=True,
        default=4,
        max_value=24,
        help_text="how many hours ahead should the schedule be fetched",
    )
    num_updated = serializers.IntegerField(
        read_only=True,
    )


class SyncAppSerializer(serializers.Serializer):
    app_labels = serializers.ListField(
        child=serializers.ChoiceField(
            choices=SYNC_APP_LABELS,
        ),
    )
    limit = serializers.IntegerField(
        allow_null=True,
        default=100,
        max_value=2000,
        help_text="limit number if items per app to sync each run",
    )
    max_age = serializers.IntegerField(
        allow_null=True,
        default=24 * 60 * 60,
        max_value=7 * 24 * 60 * 60,
        help_text="max age / last time updated before n seconds",
    )
    updated = serializers.JSONField(
        read_only=True,
    )
