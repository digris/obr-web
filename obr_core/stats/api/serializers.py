from api_extra.serializers import CTUIDModelSerializer, DurationInSecondsSerializer
from rest_framework import serializers
from stats.models import Heartbeat, PlayerEvent, StreamEvent


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


class PlayerEventSerializer(
    CTUIDModelSerializer,
):
    time_start = serializers.DateTimeField(source="time")
    time_end = serializers.DateTimeField()
    duration = DurationInSecondsSerializer(source="annotated_duration")

    class Meta(CTUIDModelSerializer.Meta):
        model = PlayerEvent
        fields = CTUIDModelSerializer.Meta.fields + [
            "id",
            "time_start",
            "time_end",
            "obj_key",
            "state",
            "source",
            "user_identity",
            "device_key",
            #
            "duration",
        ]


class ProcessedPlayerEventSerializer(
    CTUIDModelSerializer,
):
    time_start = serializers.DateTimeField(source="time")
    time_end = serializers.DateTimeField()
    # NOTE: field is decimal, but we want a number in the API
    duration = serializers.FloatField(source="calculated_duration_s")

    class Meta(CTUIDModelSerializer.Meta):
        model = PlayerEvent
        fields = CTUIDModelSerializer.Meta.fields + [
            "id",
            "time_start",
            "time_end",
            "obj_key",
            "state",
            "source",
            "user_identity",
            "device_key",
            #
            "duration",
        ]


class StreamEventSerializer(
    CTUIDModelSerializer,
):
    referer = serializers.CharField(
        allow_blank=True,
    )

    geoip_country = serializers.CharField(
        read_only=True,
        source="geoip_country.code",
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = StreamEvent
        fields = CTUIDModelSerializer.Meta.fields + [
            "origin",
            "ip",
            "path",
            "method",
            "status",
            "bytes_sent",
            "referer",
            "user_agent",
            "device_key",
            "seconds_connected",
            "time_start",
            "time_end",
            "geoip_city",
            "geoip_region",
            "geoip_country",
        ]


class PlayerEventProcessSerializer(
    serializers.Serializer,
):
    num_processed = serializers.IntegerField()


class HeartbeatCreateSerializer(
    CTUIDModelSerializer,
):
    in_foreground = serializers.BooleanField(
        default=False,
    )

    player_source = serializers.ChoiceField(
        choices=[
            "live",
            "news",
            "ondemand",
            "unknown",
        ],
    )

    player_state = serializers.ChoiceField(
        choices=[
            "playing",
            "stopped",
            "paused",
            "buffering",
        ],
    )

    class Meta(CTUIDModelSerializer.Meta):
        model = Heartbeat
        fields = CTUIDModelSerializer.Meta.fields + [
            "in_foreground",
            "player_source",
            "player_state",
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
