from api_extra.serializers import CTUIDModelSerializer
from identifier.models import Identifier
from rest_framework import serializers


class IdentifierSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    class Meta:
        model = Identifier
        fields = CTUIDModelSerializer.Meta.fields + [
            "scope",
            "value",
        ]
