from rest_framework import serializers
from .models import Match, League, Team

# Serializer per la Squadra
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country']

# Serializer per la Lega
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'name', 'color']

# Serializer per la Partita
class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    league = LeagueSerializer()

    class Meta:
        model = Match
        fields = ['id', 'home_team', 'away_team', 'date', 'score_home', 'score_away', 'is_cancelled', 'league']
