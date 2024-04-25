from api_extra.serializers import CTUIDModelSerializer
from rest_framework import serializers

from ..models import NewsSurveySubmission


class NewsSurveySubmissionSerializer(
    CTUIDModelSerializer,
    serializers.ModelSerializer,
):
    class Meta(CTUIDModelSerializer.Meta):
        model = NewsSurveySubmission
        fields = CTUIDModelSerializer.Meta.fields + [
            "is_interested",
            "news_sources",
            "comment",
        ]
