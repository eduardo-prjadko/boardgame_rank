from django.contrib import admin

from .models import Season, Match, Boardgame, MatchPlayer, SeasonPlayer


class BoardgameAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class SeasonPlayerInLine(admin.TabularInline):
    model = SeasonPlayer
    extra = 1


class SeasonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SeasonPlayerInLine]


class MatchPlayerInLine(admin.TabularInline):
    model = MatchPlayer
    extra = 1


class MatchAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [MatchPlayerInLine]


admin.site.register(Boardgame, BoardgameAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Match, MatchAdmin)
