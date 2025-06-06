from django.contrib import admin

from .models import Season, Match, Boardgame


class BoardgameAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SeasonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class MatchAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Boardgame, BoardgameAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Match, MatchAdmin)
