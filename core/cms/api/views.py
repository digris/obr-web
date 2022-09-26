from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from . import serializers
from ..page import Page


class PageView(APIView):
    @staticmethod
    @extend_schema(
        responses={
            200: serializers.PageSerializer,
        },
    )
    def get(request, path, *args, **kwargs):
        try:
            page = Page(path=path)
            return Response(
                page.as_markdown(),
            )
        except ImproperlyConfigured as e:
            raise APIException(e) from e
        except Page.PageNotFound as e:
            raise Http404(e) from e
