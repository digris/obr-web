from rest_framework import serializers

from ..models import PlayerEvent


class PlayerEventSerializer(
    serializers.ModelSerializer,
):

    obj_key = serializers.CharField(
        write_only=True,
    )

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
        write_only=True,
        required=False,
        help_text="Unix timestamp when event was created on the client.",
    )

    time = serializers.DateTimeField(
        # read_only=True,
    )

    user_identity = serializers.CharField(
        read_only=True,
    )

    device_key = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = PlayerEvent
        fields = [
            "obj_key",
            "source",
            "state",
            "ts",
            "time",
            "user_identity",
            "device_key",
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
