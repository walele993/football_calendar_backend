import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Match
from .serializers import MatchSerializer

class MatchListView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class MatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

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
