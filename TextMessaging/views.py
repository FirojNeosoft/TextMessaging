import logging

from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('sms'))
        else:
            messages.error(request, 'Please check credentials.')
            return HttpResponseRedirect(reverse('login'))


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return render(request, 'login.html')


class ChangePasswordView(LoginRequiredMixin, View):
    """
    Change Password
    """
    def get(self, request):
        """
          dashboard
        """
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        """
          change password
        """

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Error occured while changing password, please enter a proper password.')
        return redirect('change_password')
