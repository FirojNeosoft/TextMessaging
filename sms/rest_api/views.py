import logging

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import generics, status, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from sms.rest_api.serializers import *
from sms.utils import *


logger = logging.getLogger('message_log')


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
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not self.request.user.is_staff:
            queryset = User.objects.filter(id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = Application.objects.exclude(status='Delete')

        if not self.request.user.is_staff:
            queryset = Application.objects.filter(app_admin=self.request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SendMessage(generics.CreateAPIView):
    """
    Send Message.
    """
    serializer_class = MobileMessageSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            serializer = MobileMessageSerializer(data=request.data)
            if serializer.is_valid():
                if 'app_id' in serializer.data:
                    app = Application.objects.get(id=int(serializer.data['app_id']))
                    if not is_application_or_system_admin(request, app.id):
                        return Response({'status': 400,
                                         'message': 'You don\'t have permission to send sms for this application.'},\
                                        status=status.HTTP_400_BAD_REQUEST)

                    if is_application_expire(app.id):
                        return Response({'status': 400, 'message': 'Selected application is expired'},\
                                        status=status.HTTP_400_BAD_REQUEST)
                    message_log = send_sms(serializer.data['send_to'], serializer.data['message'])
                    message_log.application = app
                    message_log.save()
                else:
                    send_sms(serializer.data['send_to'], serializer.data['message'])
                return Response({'status': 201, 'message':'SMS sent successfully'}, status=status.HTTP_201_CREATED)
            logger.error("Fail to send sms")
            return Response({'status': 400, 'message':'Fail to send SMS'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error occured while sending sms "+str(e))
            return Response({'status': 400, 'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
