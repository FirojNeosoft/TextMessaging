import plivo

from django.conf import settings

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from sms.models import *
from sms.utils import *


class ListApplicationsView(LoginRequiredMixin, ListView):
    """
    List applications
    """
    model = Application
    queryset = Application.objects.exclude(status='Delete')
    template_name = 'application_list.html'


class CreateApplicationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new application
    """
    model = Application
    fields = ['name', 'max_limit', 'status']
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
                # client = plivo.RestClient(settings.PLIVO_AUTH_ID, settings.PLIVO_AUTH_TOKEN)
                # client.messages.create(src=settings.SENDER_NUMBER, dst=request.POST['send_to'],\
                #                    text=request.POST['text_message'], )
                form.save()
                messages.success(request, "Successfully SMS sent.")


        except Exception as e:
            messages.error(request, "Error occured while sending sms.")
        return redirect('sms')

