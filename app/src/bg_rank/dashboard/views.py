from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from .forms import BoardgameForm, MatchForm, SeasonForm
from .models import Boardgame


def main(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard/test.html")


def match(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard/match/match.html")


def season(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard/season/season.html")


class BoardgameFormView(FormView):
    template_name = "dashboard/boardgame/create.html"
    form_class = BoardgameForm
    success_url = "/boardgame/"

    def form_valid(self, form: BoardgameForm) -> HttpResponse:
        # form.send_email()
        form.save()
        return super().form_valid(form)


class MatchFormView(FormView):
    template_name = "dashboard/match/create.html"
    form_class = MatchForm
    success_url = "/match/"

    def form_valid(self, form: MatchForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)


class SeasonFormView(FormView):
    template_name = "dashboard/season/create.html"
    form_class = SeasonForm
    success_url = "/season/"

    def form_valid(self, form: SeasonForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)


User = get_user_model()


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "dashboard/player/detail.html"

    def get_object(self):
        return self.request.user


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "dashboard/player/change_password.html"
    success_url = reverse_lazy("player_profile")

    def form_valid(self, form):
        messages.success(self.request, "Senha alterada com sucesso!")
        return super().form_valid(form)


class BoardGameListView(ListView):
    model = Boardgame
    template_name = "dashboard/boardgame/boardgame.html"
    context_object_name = "boardgames"
