from api_extra.serializers import CTUIDModelSerializer
from rest_framework import serializers

from ..models import Page, Section


class SectionSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    title = serializers.CharField(
        read_only=True,
    )
    expandable = serializers.BooleanField(
        read_only=True,
    )
    body = serializers.CharField(
        read_only=True,
        source="render",
    )

    class Meta:
        model = Section
        fields = CTUIDModelSerializer.Meta.fields + [
            "ct",
            "uid",
            "title",
            "expandable",
            "body",
            "cta_title",
            "cta_url",
        ]


class PageSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    title = serializers.CharField(
        read_only=True,
    )
    lead = serializers.CharField(
        source="render_lead",
        read_only=True,
    )
    sections = SectionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Page
        fields = CTUIDModelSerializer.Meta.fields + [
            "ct",
            "uid",
            "title",
            "lead",
            "sections",
        ]


class StaticPageSerializer(
    serializers.Serializer,
):
    title = serializers.CharField(
        read_only=True,
    )
    lead = serializers.CharField(
        read_only=True,
    )
    sections = serializers.JSONField(
        read_only=True,
    )
