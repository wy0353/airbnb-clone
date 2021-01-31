from django.shortcuts import render
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings


def language_switch_view(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        translation.activate(lang)
        res = HttpResponse(status=200)
        res.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return res
