from rest_framework import serializers


class SyncScheduleSerializer(serializers.Serializer):
    num_hours = serializers.IntegerField(
        allow_null=True,
        default=4,
        max_value=24,
    )
    num_updated = serializers.IntegerField(
        read_only=True,
    )
