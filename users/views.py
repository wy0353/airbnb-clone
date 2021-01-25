import os
import requests
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from . import forms as user_forms
from . import models as user_models


class UserJoinView(FormView):

    """ User Join View Definition """

    template_name = "users/join.html"
    form_class = user_forms.JoinForm
    success_url = reverse_lazy("core:home")
    initial = {
        # "first_name": "Two",
        # "last_name": "Tester",
        # "email": "wy0353@gmail.com",
    }

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        user.verify_email()
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


def complete_verification(request, key):
    try:
        user = user_models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = None
        user.save()
        # to do: add success message
    except user_models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


def github_login(request):
    client_id = os.environ.get("GITHUB_CLIENT_ID")
    redirect_url = "http://121.130.15.124:8003/users/login/github/callback/"
    scopes = "read:user"
    base_url = "https://github.com/"
    prefix = "login/oauth/authorize"
    query = f"?client_id={client_id}&redirect_url={redirect_url}&scope={scopes}"
    full_url = f"{base_url}{prefix}{query}"

    return redirect(full_url)


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        code = request.GET.get("code", None)    
        if code is not None:
            client_id = os.environ.get("GITHUB_CLIENT_ID")
            client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
            print(code)
            base_url = "https://github.com/"
            prefix = "login/oauth/access_token"
            query = f"?client_id={client_id}&client_secret={client_secret}&code={code}"
            full_url = f"{base_url}{prefix}{query}"
            res = requests.post(full_url, headers={
                "Accept": "application/json"
            })
            results = res.json()
            error = results.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = results.get("access_token")
                user_results = requests.get("https://api.github.com/user", headers={
                    "Accept": "application/json",
                    "Authorization": f"token {access_token}",
                })
                github_user = user_results.json()
                username = github_user.get("login", None)
                if username is not None:
                    name = github_user.get("name")
                    email = github_user.get("email")
                    bio = github_user.get("bio")
                    try:
                        user = user_models.User.objects.get(email=email)
                        if user.login_method != user_models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except user_models.User.DoesNotExist:
                        user = user_models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=user_models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_CLIENT_ID", None)
    if client_id is not None:
        redirect_uri = "http://121.130.15.124:8003/users/login/kakao/callback/"
        base_url = "https://kauth.kakao.com/"
        prefix = "oauth/authorize"
        query = f"?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        full_url = f"{base_url}{prefix}{query}"
        return redirect(full_url)
    
    return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code", None)
        if code is not None:
            client_id = os.environ.get("KAKAO_CLIENT_ID", None)
            client_secret = os.environ.get("KAKAO_CLIENT_SECRET", None)
            redirect_uri = "http://121.130.15.124:8003/users/login/kakao/callback/"
            base_url = "https://kauth.kakao.com/"
            prefix = "oauth/token"
            query = f"?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}"
            full_url = f"{base_url}{prefix}{query}"
            res = requests.post(full_url, headers={
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
            })
            results = res.json()
            error = results.get("error", None)
            if error is not None:
                raise KakaoException()
            access_token = results.get("access_token")

            base_url = "https://kapi.kakao.com/"
            prefix = "v2/user/me"
            full_url = f"{base_url}{prefix}"
            res = requests.get(full_url, headers={
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                "Authorization": f"Bearer {access_token}"
            })
            results = res.json()
            properties = results.get("properties")
            email = results["kakao_account"]["email"]
            name = properties.get("nickname", None)
            profile_image = properties.get("profile_image", None)
            thumbnail_image = properties.get("thumbnail_image", None)
            try:
                user = user_models.User.objects.get(email=email)
                if user.login_method != user_models.User.LOGIN_KAKAO:
                    raise KakaoException()

            except user_models.User.DoesNotExist:
                user = user_models.User.objects.create(
                    email=email,
                    first_name=name,
                    username=email,
                    login_method=user_models.User.LOGIN_KAKAO,
                    email_verified=True,
                )
                user.set_unusable_password()
                user.save()
                if profile_image is not None:
                    photo_res = requests.get(profile_image)                    
                    user.avatar.save(f"{name}-avatar.png", ContentFile(photo_res.content))
            login(request, user)
            return redirect(reverse("core:home"))            
        else:
            raise KakaoException()
    except KakaoException:
        return redirect(reverse("users:login"))
