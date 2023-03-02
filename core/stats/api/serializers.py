from rest_framework import serializers


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


class ArchiveSerializer(
    serializers.Serializer,
):
    num_airplays_archived = serializers.IntegerField(
        read_only=True,
    )
    num_emissions_archived = serializers.IntegerField(
        read_only=True,
    )
