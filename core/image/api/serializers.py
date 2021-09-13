# -*- coding: utf-8 -*-
from rest_framework import serializers
from image.models import BaseImage



class BaseImageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            "ct",
            "uid",
            "url",
            "path",
            "rgb",
        ]
        abstract = True


class ImageSerializer(serializers.Serializer):
    def to_representation(self, instance):
        if not instance:
            return None

        data = {
            "file": instance.file.name,
            "path": instance.path,
            "url": instance.url,
            "rgb": instance.rgb,
        }

        return data
