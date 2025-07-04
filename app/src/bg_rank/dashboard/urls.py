from django.urls import path

from . import views


urlpatterns = [
    path("main/", views.main),
    path("boardgame/", views.boardgame),
    path("boardgame/create/", views.BoardgameFormView.as_view()),
    path("match/", views.match),
    path("match/create/", views.MatchFormView.as_view()),
]
