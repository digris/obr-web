# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse_lazy, reverse
from django.conf import settings

from rest_framework import serializers


from ..models import Vote

# SITE_URL = getattr(settings, 'SITE_URL')


class VoteSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField()

    class Meta:
        model = Vote
        depth = 1
        fields = [
            "key",
            "value",
            "updated",
        ]
