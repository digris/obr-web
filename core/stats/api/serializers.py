from api_extra.serializers import CTUIDModelSerializer
from rest_framework import serializers
from stats.models import StreamEvent


class PlayerEventCreateSerializer(
    serializers.Serializer,
):
    obj_key = serializers.CharField()

    source = serializers.ChoiceField(
        choices=[
            "live",
            "on-demand",
        ],
    )

    state = serializers.ChoiceField(
        choices=[
            "playing",
            "stopped",
            "paused",
            "buffering",
        ],
    )

    ts = serializers.IntegerField(
        help_text="Unix timestamp when event was created on the client.",
    )


class StreamEventSerializer(
    CTUIDModelSerializer,
):
    referer = serializers.CharField(
        allow_blank=True,
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = StreamEvent
        fields = CTUIDModelSerializer.Meta.fields + [
            "ip",
            "path",
            "method",
            "status",
            "bytes_sent",
            "referer",
            "user_agent",
            "seconds_connected",
            "time_start",
            "time_end",
        ]


class ArchiveSerializer(
    serializers.Serializer,
):
    num_airplays_archived = serializers.IntegerField(
        read_only=True,
    )
    num_emissions_archived = serializers.IntegerField(
        read_only=True,
    )
