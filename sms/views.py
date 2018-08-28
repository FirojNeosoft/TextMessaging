import plivo

from django.conf import settings

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class SMSView(LoginRequiredMixin, View):
    """
    send SMS
    """
    def get(self, request):
        return render(request, 'sms_form.html')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """

        try:
            if request.POST['mobile'] and request.POST['message']:
                client = plivo.RestClient(settings.PLIVO_AUTH_ID, settings.PLIVO_AUTH_TOKEN)
                client.messages.create(src=settings.SENDER_NUMBER, dst=request.POST['mobile'],\
                                   text=request.POST['message'], )
                messages.success(request, "Successfully SMS sent.")
        except Exception as e:
            messages.error(request, "Error occured while sending sms.")
        return redirect('sms')
