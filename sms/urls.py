from django.contrib import admin
from django.urls import path, include

from sms.views import *


urlpatterns = [
    path('users/', ListUsersView.as_view(), name='list_users'),
    path('user/add/', CreateUserView.as_view(), name='add_user'),
    path('user/<int:pk>/edit/', UpdateUserView.as_view(), name='update_user'),
    path('user/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),

    path('applications/', ListApplicationsView.as_view(), name='list_applications'),
    path('application/add/', CreateApplicationView.as_view(), name='add_application'),
    path('application/<int:pk>/edit/', UpdateApplicationView.as_view(), name='update_application'),
    path('application/<int:pk>/delete/', DeleteApplicationView.as_view(), name='delete_application'),
    
    path('', SMSView.as_view(), name='sms'),
    path('logs/', LogsView.as_view(), name='sms_logs'),
]