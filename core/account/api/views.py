# -*- coding: utf-8 -*-
import logging
import time

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count

from rest_framework import mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.compat import coreapi
from rest_framework.compat import coreschema
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters

from ..models import User
from . import serializers


logger = logging.getLogger(__name__)


class CurrentUserView(APIView):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            serializer = serializers.UserSerializer(
                request.user,
                context={
                    "request": request,
                },
            )
            return Response(serializer.data)
        else:
            return Response()


class LoginView(APIView):
    @staticmethod
    def post(request):
        user = authenticate(**request.data)
        if user is not None:
            login(request, user)
            serializer = serializers.UserSerializer(
                user,
                context={
                    "request": request,
                },
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                "error": "invalid login",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    @staticmethod
    def post(request):
        logout(request)
        return Response(
            None,
            status=status.HTTP_205_RESET_CONTENT,
        )


# class UserViewSet(
#     mixins.RetrieveModelMixin,
#     viewsets.GenericViewSet,
# ):
#     """
#     User endpoint ("me").
#     """
#
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#     lookup_field = "uid"
#
#     def get_queryset(self):
#         return self.queryset.filter(id=self.request.user.id)
#
#     def get_object(self):
#         try:
#             obj_uid = self.kwargs["uid"]
#             assert len(obj_uid) == 8
#         except AssertionError:
#             raise ParseError(f"Invalid UID: {self.kwargs['uid']}")
#
#         obj = get_object_or_404(self.get_queryset(), uid=obj_uid)
#
#         return obj
#
#     def retrieve(self, request, *args, **kwargs):
#         """
#         If provided 'uid' is "me" then return the current user.
#         """
#         if kwargs.get("uid") == "me":
#             if request.user.is_authenticated:
#                 return Response(self.get_serializer(request.user).data)
#             else:
#                 return Response()
#         return super().retrieve(request, args, kwargs)
