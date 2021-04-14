# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_framework import serializers

from account.models import User


SITE_URL = getattr(settings, "SITE_URL")

logger = logging.getLogger(__name__)


# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            # "url",
            "ct",
            "uid",
            # "uuid",
            "email",
        ]
