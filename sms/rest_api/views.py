import plivo

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import generics, status, viewsets, filters
from rest_framework.permissions import IsAdminUser

from sms.rest_api.serializers import *
from sms.utils import *


class UserViewSet(viewsets.ModelViewSet):
    """
    Work on user entity
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('username', 'email')
    ordering_fields = ('username', 'email')
    filter_fields = ('username', 'email', 'is_staff')


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    Work on application entity
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name', 'status')
    ordering_fields = ('name', 'created_at')
    filter_fields = ('name',)


class SendMessage(generics.CreateAPIView):
    """
    Send Message.
    """
    serializer_class = MobileMessageSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, format=None):
        if is_application_expire(request.POST['app_id']):
            serializer = MobileMessageSerializer(data=request.data)
            if serializer.is_valid():
                client = plivo.RestClient(settings.PLIVO_AUTH_ID, settings.PLIVO_AUTH_TOKEN)
                client.messages.create(src=settings.SENDER_NUMBER, dst=serializer.data['send_to'],\
                                       text=serializer.data['message'], )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'success': False,
                'message': 'Selected application is expired.',
                'data':{}
            })
