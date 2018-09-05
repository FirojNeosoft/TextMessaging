import plivo
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from sms.models import *
from sms.utils import *


logger = logging.getLogger('message_log')


class ListUsersView(LoginRequiredMixin, ListView):
    """
    List Users
    """
    model = User
    queryset = User.objects.all()
    template_name = 'user_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        queryset = User.objects.all()
        if not self.request.user.is_staff:
            queryset = User.objects.filter(id=self.request.user.id)
        return queryset


class CreateUserView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was created successfully"
    success_url = reverse_lazy('list_users')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password'])
            user.save()
        else:
            logger.error(form.errors)
            messages.error(request, form.errors)
            return redirect('add_user')
        messages.success(request, "{}, user added successfully.".format(user.username))
        return HttpResponseRedirect(reverse('list_users'))


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing user
    """
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'user_form.html'
    success_message = "%(username)s was updated successfully"
    success_url = reverse_lazy('list_users')


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """
    Delete existing user
    """
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = reverse_lazy('list_users')


class ListApplicationsView(LoginRequiredMixin, ListView):
    """
    List applications
    """
    model = Application
    queryset = Application.objects.exclude(status='Delete')
    template_name = 'application_list.html'

    def get_queryset(self):
        """
        Return the list of items for this view.
        """
        queryset = Application.objects.exclude(status='Delete')
        if not self.request.user.is_staff:
            queryset = Application.objects.filter(app_admin=self.request.user.id)
        return queryset


class CreateApplicationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new application
    """
    model = Application
    fields = ['name', 'app_admin', 'max_limit', 'status']
    template_name = 'application_form.html'
    success_message = "%(name)s was created successfully"
    success_url = reverse_lazy('list_applications')


class UpdateApplicationView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update existing application
    """
    model = Application
    fields = ['name', 'max_limit', 'status']
    template_name = 'application_form.html'
    success_message = "%(name)s was updated successfully"
    success_url = reverse_lazy('list_applications')


class DeleteApplicationView(LoginRequiredMixin, DeleteView):
    """
    Delete existing application
    """
    model = Application
    template_name = 'application_confirm_delete.html'
    success_url = reverse_lazy('list_applications')


class SMSView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    send SMS
    """
    model = TextMessageHistory
    fields = ['application', 'send_to', 'text_message']
    template_name = 'sms_form.html'
    success_message = "SMS sent successfully"
    success_url = reverse_lazy('sms')

    def get_context_data(self, **kwargs):
        context = super(SMSView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['form'].fields['application'].queryset = Application.objects.exclude(status='Delete')
        else:
            context['form'].fields['application'].queryset = Application.objects.filter(app_admin=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """

        try:
            if request.POST['application']:
                if is_application_expire(request.POST['application']):
                    messages.error(request, "Selected application is expired.")
                    return redirect('sms')

            form = self.get_form()
            if form.is_valid():
                client = plivo.RestClient(settings.PLIVO_AUTH_ID, settings.PLIVO_AUTH_TOKEN)
                client.messages.create(src=settings.SENDER_NUMBER, dst=request.POST['send_to'],\
                                   text=request.POST['text_message'], )
                form.save()
                messages.success(request, "Successfully SMS sent.")

        except Exception as e:
            logger.error("Error occured while sending sms "+str(e))
            messages.error(request, "Error occured while sending sms.")
        return redirect('sms')

