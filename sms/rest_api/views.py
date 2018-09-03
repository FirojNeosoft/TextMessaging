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
        try:
            serializer = MobileMessageSerializer(data=request.data)
            if serializer.is_valid():
                if 'app_id' in serializer.data:
                    app = Application.objects.get(id=int(serializer.data['app_id']))
                    if is_application_expire(app.id):
                        return Response({'status':400, 'message':'Selected application is expired'},\
                                        status=status.HTTP_400_BAD_REQUEST)
                    message_log = send_sms(serializer.data['send_to'], serializer.data['message'])
                    message_log.application = app
                    message_log.save()
                else:
                    send_sms(serializer.data['send_to'], serializer.data['message'])
                return Response({'status':201, 'message':'SMS sent successfully'}, status=status.HTTP_201_CREATED)
            return Response({'status':400, 'message':'Fail to send SMS'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':400, 'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
