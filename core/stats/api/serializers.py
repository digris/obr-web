from rest_framework import serializers

from ..models import PlayerEvent


class PlayerEventSerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = PlayerEvent
        exclude = ("id",)


class ArchiveSerializer(
    serializers.Serializer,
):
    num_airplays_archived = serializers.IntegerField(
        read_only=True,
    )
    num_emissions_archived = serializers.IntegerField(
        read_only=True,
    )
