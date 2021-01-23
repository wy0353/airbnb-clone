from django.views import View
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from . import forms as user_forms


class UserJoinView(FormView):

    """ User Join View Definition """

    template_name = "users/join.html"
    form_class = user_forms.JoinForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Two",
        "last_name": "Tester",
        "email": "tester2@email.com",
    }

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class UserLoginView(FormView):

    """ User Login View Definition """

    template_name = "users/login.html"
    form_class = user_forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            user.email = email
            user.save()        
        return super().form_valid(form)


class UserLogoutView(LogoutView):

    """ User Logout View Definition """

    next_page = reverse_lazy("core:home")
