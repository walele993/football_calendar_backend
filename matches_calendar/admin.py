from django.contrib import admin
from .models import Match, Team

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('matchday', 'date', 'home_team', 'away_team', 'score_home', 'score_away', 'competition', 'season', 'is_cancelled')
    list_filter = ('competition', 'is_cancelled', 'home_team', 'away_team')
    search_fields = ('matchday', 'home_team__name', 'away_team__name', 'competition', 'season')
    ordering = ('-date',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
