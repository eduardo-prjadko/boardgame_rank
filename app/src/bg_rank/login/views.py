from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def login(request: HttpRequest) -> HttpResponse:
    return render(request, "login/login.html")


def register(request: HttpRequest) -> HttpResponse:
    return render(request, "login/register.html")
