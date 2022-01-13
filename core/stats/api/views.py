import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers


logger = logging.getLogger(__name__)

# @method_decorator(
#     csrf_exempt,
#     name="dispatch",
# )
class PlayerEventView(APIView):
    serializer_class = serializers.PlayerEventSerializer

    def put(self, request, format=None):

        events = request.data.get('events', [])

        for event in events:
            event['user_identity'] = request.user_identity
            logger.info('player-event', event)

        print('events', events)

        return Response(
            None,
            status.HTTP_201_CREATED,
        )
