import os
import json
from django.db import models
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Match, League, Team
from .serializers import MatchSerializer, LeagueSerializer, TeamSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from utils.mongo import matches_collection
from datetime import datetime
from utils.mongo import create_indexes

create_indexes()

# --- Squadre ---
class TeamListView(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

# --- Leghe ---
class LeagueListView(generics.ListCreateAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

class LeagueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

# --- Partite ---
class MatchListView(generics.ListCreateAPIView):
    serializer_class = MatchSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Match.objects.select_related('home_team', 'away_team', 'league').all()

        league_id = self.request.query_params.get('league')
        if league_id:
            queryset = queryset.filter(league__id=league_id)

        team_id = self.request.query_params.get('team')
        if team_id:
            queryset = queryset.filter(
                models.Q(home_team__id=team_id) | models.Q(away_team__id=team_id)
            )

        date = self.request.query_params.get('date')
        if date:
            try:
                filter_date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
                queryset = queryset.filter(date=filter_date)
            except ValueError:
                pass

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            try:
                start = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                end = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__range=(start, end))
            except ValueError:
                pass

        return queryset.order_by('date')

class MatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.select_related('home_team', 'away_team', 'league').all()
    serializer_class = MatchSerializer

# --- Partite da file JSON locale (debug/test) ---
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

@api_view(["GET"])
def all_matches_mongo(request):
    matches = list(matches_collection.find({}, {"_id": 0}).sort("date", 1).limit(1000))
    return Response(matches)

@api_view(["GET"])
def all_leagues_mongo(request):
    leagues = matches_collection.distinct("league")
    return Response(leagues)

@api_view(["GET"])
def all_teams_mongo(request):
    teams = matches_collection.aggregate([
        {"$project": {"teams": ["$home_team", "$away_team"]}},
        {"$unwind": "$teams"},
        {"$group": {"_id": "$teams.id", "name": {"$first": "$teams.name"}}},
        {"$project": {"id": "$_id", "name": 1, "_id": 0}},
        {"$sort": {"name": 1}}
    ])
    return Response(list(teams))

@api_view(["GET"])
def filter_matches_mongo(request):
    query = {}
    
    # Filter by league
    league_id = request.query_params.get("league")
    if league_id:
        try:
            query["league.id"] = int(league_id)
        except ValueError:
            return Response({"error": "Invalid league id"}, status=400)

    # Filter by team (either home or away)
    team_id = request.query_params.get("team")
    if team_id:
        try:
            team_id = int(team_id)
            query["$or"] = [{"home_team.id": team_id}, {"away_team.id": team_id}]
        except ValueError:
            return Response({"error": "Invalid team id"}, status=400)

    # Filter by single date
    date = request.query_params.get("date")
    if date:
        parsed_date = parse_date(date)
        if parsed_date:
            query["date"] = parsed_date.strftime("%Y-%m-%d")
        else:
            return Response({"error": "Invalid date format"}, status=400)

    # Filter by date range
    start = request.query_params.get("start_date")
    end = request.query_params.get("end_date")
    if start and end:
        try:
            start_d = datetime.strptime(start, "%Y-%m-%d").date().isoformat()
            end_d = datetime.strptime(end, "%Y-%m-%d").date().isoformat()
            query["date"] = {"$gte": start_d, "$lte": end_d}
        except ValueError:
            return Response({"error": "Invalid date range format"}, status=400)

    matches = list(matches_collection.find(query, {"_id": 0}).sort("date", 1).limit(1000))
    return Response(matches)
