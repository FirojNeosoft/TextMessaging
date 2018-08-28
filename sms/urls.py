from django.contrib import admin
from django.urls import path, include

from sms.views import *


urlpatterns = [
             path('', SMSView.as_view(), name='sms'),
]