from rest_framework import serializers
from .models import Match, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country']

class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()

    class Meta:
        model = Match
        fields = ['id', 'home_team', 'away_team', 'date', 'score_home', 'score_away', 'is_cancelled', 'competition', 'season']
