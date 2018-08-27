import plivo

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from sms.rest_api.serializers import *


class SendMessage(generics.CreateAPIView):
    """
    Send Message.
    """
    serializer_class = MobileMessageSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, format=None):
        serializer = MobileMessageSerializer(data=request.data)
        if serializer.is_valid():
            client = plivo.RestClient(settings.PLIVO_AUTH_ID, settings.PLIVO_AUTH_TOKEN)
            client.messages.create(src=settings.SENDER_NUMBER, dst=serializer.data['send_to'],\
                                   text=serializer.data['message'], )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
