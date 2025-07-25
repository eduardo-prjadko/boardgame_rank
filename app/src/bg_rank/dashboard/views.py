from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import FormView

from .forms import BoardgameForm, MatchForm, SeasonForm


def main(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard/test.html")


def boardgame(request: HttpRequest) -> HttpResponse:
    return render(request, "dashboard/boardgame/boardgame.html")


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
