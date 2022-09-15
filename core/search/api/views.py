import logging
import bleach

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SearchResultSerializer
from .. import global_search

log = logging.getLogger(__name__)


class GlobalSearchView(APIView):
    def get(self, request):

        q = request.GET.get("q")

        results = global_search.get_results(q=q)

        serializer = SearchResultSerializer(
            results,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
