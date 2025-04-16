from django.contrib import admin
from .models import Match, Team, League

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('matchday', 'date', 'home_team', 'away_team', 'score_home', 'score_away', 'league', 'season', 'is_cancelled')
    list_filter = ('league', 'is_cancelled', 'home_team', 'away_team')
    search_fields = ('matchday', 'home_team__name', 'away_team__name', 'league__name', 'season')
    ordering = ('-date',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
