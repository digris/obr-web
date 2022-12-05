from identifier.models import Identifier
from rest_framework import serializers


class IdentifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identifier
        fields = [
            "ct",
            "uid",
            "scope",
            "value",
        ]
