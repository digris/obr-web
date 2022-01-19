from rest_framework import serializers
from ..models import PlayerEvent


class PlayerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerEvent
        exclude = ("id",)
