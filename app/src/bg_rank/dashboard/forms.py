from django import forms
from django.utils.text import slugify
from django.contrib.auth.models import User
from .models import Boardgame, Match, Season
import django_select2.forms as s2forms


class BoardgameForm(forms.ModelForm):
    class Meta:
        model = Boardgame
        fields = ("name",)
        labels = {"name": "Nome do jogo"}
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self):
        instance = super().save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.name)
        instance.save()
        return instance


class PlayerWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = ["username__icontains"]

    def __init__(self, *args, **kwargs):
        attrs = {
            "class": "form-control",
        }
        super().__init__(
            model=User,
            attrs=attrs,
            *args,
            **kwargs,
        )


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = (
            "name",
            "boardgame_id",
            "season_id",
            "enrolled_players",
            "is_friendly",
            "start_at",
            "end_at",
        )
        labels = {
            "name": "Nome da partida",
            "boardgame_id": "Jogo",
            "season_id": "Temporada",
            "enrolled_players": "Jogadores",
            "is_friendly": "Amistoso",
            "start_at": "Início",
            "end_at": "Fim",
        }
        widgets = {
            "enrolled_players": PlayerWidget,
        }
        querysets = {"enrolled_players": User.objects.all()}


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season
        fields = (
            "name",
            "enrolled_players",
            "start_at",
            "end_at",
        )
        labels = {
            "name": "Nome da temporada",
            "enrolled_players": "Jogadores",
            "start_at": "Início",
            "end_at": "Fim",
        }
        widgets = {
            "enrolled_players": PlayerWidget,
        }
        querysets = {"enrolled_players": User.objects.all()}
