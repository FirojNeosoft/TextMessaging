from django.urls import path, include

from rest_framework import routers

from sms.rest_api.views import *

router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('send/', SendMessage.as_view()),
    ]