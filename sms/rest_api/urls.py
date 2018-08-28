from django.urls import path, include

from rest_framework import routers

from sms.rest_api.views import *

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send/', SendMessage.as_view()),
    ]