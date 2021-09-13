# -*- coding: utf-8 -*-
from rest_framework import serializers


class CTUIDModelSerializer(serializers.Serializer):
    uid = serializers.CharField(
        min_length=8,
        max_length=8,
        help_text="UID",
    )
