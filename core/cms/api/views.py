from django.http import Http404

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Page
from . import serializers


class PageView(APIView):
    @staticmethod
    @extend_schema(
        responses={
            200: serializers.PageSerializer,
        },
        operation_id="page",
        auth=[],
    )
    def get(request, path, *args, **kwargs):
        try:
            page = Page.objects.get(path=path)
            serializer = serializers.PageSerializer(page)
            return Response(
                serializer.data,
            )
        except Page.DoesNotExist as e:
            raise Http404(e) from e
