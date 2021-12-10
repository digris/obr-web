from rest_framework import serializers
from identifier.models import Identifier


class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        fields = [
            "ct",
            "uid",
            "scope",
            "value",
        ]
