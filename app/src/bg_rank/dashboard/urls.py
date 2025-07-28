from django.urls import path

from . import views


urlpatterns = [
    path("main/", views.main),
    path("boardgame/", views.BoardGameListView.as_view(), name="boardgames"),
    path(
        "boardgame/create/", views.BoardgameFormView.as_view(), name="boardgame-create"
    ),
    path("match/", views.match),
    path("match/create/", views.MatchFormView.as_view()),
    path("season/", views.season),
    path("season/create/", views.SeasonFormView.as_view()),
    path("profile/", views.UserProfileView.as_view(), name="player_profile"),
    path(
        "profile/change_password",
        views.CustomPasswordChangeView.as_view(),
        name="change_password",
    ),
]
