import os
import json
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Match, League, Team
from .serializers import MatchSerializer, LeagueSerializer, TeamSerializer

# View per visualizzare tutte le squadre
class TeamListView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

# View per visualizzare tutte le leghe
class LeagueListView(generics.ListCreateAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

from rest_framework.pagination import PageNumberPagination

class MatchListView(generics.ListCreateAPIView):
    serializer_class = MatchSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Match.objects.all().order_by('date')

        # Filtro per lega (opzionale)
        league_id = self.request.query_params.get('league')
        if league_id:
            queryset = queryset.filter(league__id=league_id)

        # Filtro per squadra (sia in casa che fuori)
        team_id = self.request.query_params.get('team')
        if team_id:
            queryset = queryset.filter(
                models.Q(home_team__id=team_id) | models.Q(away_team__id=team_id)
            )

        return queryset[:75]


# View per visualizzare i dettagli di una singola partita
class MatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

# View per visualizzare una lista delle leghe
class LeagueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

# View per visualizzare una lista delle partite da un file locale (se necessario)
class MatchListFromLocalFile(APIView):
    def get(self, request):
        file_path = os.path.join("matches_calendar", "data", "all_matches.json")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Response(data)
        except FileNotFoundError:
            return Response({"error": "Local JSON file not found."}, status=404)
        except json.JSONDecodeError:
            return Response({"error": "Error decoding JSON file."}, status=500)
