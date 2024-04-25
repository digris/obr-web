import logging

import bleach
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import NewsSurveySubmission
from . import serializers

log = logging.getLogger(__name__)


class NewsSurveySubmissionView(
    APIView,
):
    @staticmethod
    def get_submission(request):
        kwargs = {}
        if request.user.is_authenticated:
            kwargs["user"] = request.user
        else:
            kwargs["user_identity"] = request.user_identity

        try:
            return NewsSurveySubmission.objects.get(**kwargs)

        except NewsSurveySubmission.DoesNotExist:
            return None

    @staticmethod
    def create_submission(request):
        kwargs = {}
        if request.user.is_authenticated:
            kwargs["user"] = request.user
        else:
            kwargs["user_identity"] = request.user_identity

        return NewsSurveySubmission.objects.create(**kwargs)

    @extend_schema(
        responses={
            200: serializers.NewsSurveySubmissionSerializer,
            204: None,
        },
    )
    def get(self, request):
        submission = self.get_submission(request)

        if not submission:
            return Response(
                None,
                status=status.HTTP_204_NO_CONTENT,
            )

        serializer = serializers.NewsSurveySubmissionSerializer(submission)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        methods=["POST"],
        request=serializers.NewsSurveySubmissionSerializer,
        responses={
            200: serializers.NewsSurveySubmissionSerializer,
        },
    )
    def post(self, request):
        serializer = serializers.NewsSurveySubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        submission = self.get_submission(request) or self.create_submission(request)

        submission.is_interested = serializer.validated_data["is_interested"]
        submission.news_sources = serializer.validated_data["news_sources"]
        submission.comment = bleach.clean(serializer.validated_data["comment"])

        submission.save()

        return Response(
            serializers.NewsSurveySubmissionSerializer(submission).data,
        )
