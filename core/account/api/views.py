# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.cdn_credentials.utils import (
    set_credentials,
    remove_credentials,
)
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
            response = Response(serializer.data)
            response = set_credentials(response)
        else:
            response = Response()
            response = remove_credentials(response)
        return response


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
            response = Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
            response = set_credentials(response)
        else:
            response = Response(
                {
                    "error": "invalid login",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return response


class LogoutView(APIView):
    @staticmethod
    # pylint: disable=unused-argument
    def post(request, *args, **kwargs):
        logout(request)
        response = Response(
            None,
            status=status.HTTP_205_RESET_CONTENT,
        )
        response = remove_credentials(response)
        return response


class CredentialsView(APIView):
    @staticmethod
    # pylint: disable=unused-argument
    def get(request, *args, **kwargs):
        # logger.debug("headers", request.headers)
        if request.user.is_authenticated:
            seconds_valid = 60 * 60
            logger.info(
                "refresh credentials",
                {
                    "user": str(request.user),
                    "seconds_valid": seconds_valid,
                },
            )
            response = Response(
                {
                    "seconds_valid": seconds_valid,
                },
                status=status.HTTP_200_OK,
            )
            response = set_credentials(response, seconds_valid=seconds_valid)
        else:
            response = Response(
                None,
                status=status.HTTP_204_NO_CONTENT,
            )
            response = remove_credentials(response)
        return response


class NoOpView(APIView):
    @staticmethod
    # pylint: disable=unused-argument
    def get(request, *args, **kwargs):
        print(request.user.is_authenticated)
        return Response(
            {
                "no": "op",
            },
            status=status.HTTP_200_OK,
        )
