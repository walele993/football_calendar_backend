import os
import django
from pymongo import MongoClient, UpdateOne
from dotenv import load_dotenv

# Inizializza Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "football_calendar_backend.settings")  
django.setup()

from matches_calendar.models import Match, Team, League
from django.core.serializers.json import DjangoJSONEncoder
import json

# Carica variabili d'ambiente
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")

# Verifica che l'URI venga letto correttamente
if not MONGO_URI:
    raise ValueError("MONGODB_URI non è impostato nel file .env")

print(f"Connettendosi a MongoDB URI: {MONGO_URI}")

# Connessione a MongoDB
client = MongoClient(MONGO_URI)
db = client["football_db"]
matches_collection = db["matches"]
teams_collection = db["teams"]
leagues_collection = db["leagues"]

# Serializzazione
def serialize_match(match):
    return {
        "id": match.id,
        "date": str(match.date) if match.date else None,
        "time": str(match.time) if match.time else None,
        "matchday": match.matchday,
        "season": match.season,
        "is_cancelled": match.is_cancelled,
        "score_home": match.score_home,
        "score_away": match.score_away,
        "home_team": {
            "id": match.home_team.id,
            "name": match.home_team.name,
        },
        "away_team": {
            "id": match.away_team.id,
            "name": match.away_team.name,
        },
        "league": {
            "id": match.league.id if match.league else None,
            "name": match.league.name if match.league else None,
        },
    }

def serialize_team(team):
    return {
        "id": team.id,
        "name": team.name,
    }

def serialize_league(league):
    return {
        "id": league.id,
        "name": league.name,
    }

# MIGRAZIONE MATCHES
matches = Match.objects.select_related("home_team", "away_team", "league").all()
serialized_matches = [serialize_match(m) for m in matches]
bulk_matches = [
    UpdateOne({"id": m["id"]}, {"$set": m}, upsert=True)
    for m in serialized_matches
]
if bulk_matches:
    matches_collection.bulk_write(bulk_matches)
    print(f"Migrati {len(bulk_matches)} match su MongoDB.")

# MIGRAZIONE TEAM
teams = Team.objects.all()
serialized_teams = [serialize_team(t) for t in teams]
bulk_teams = [
    UpdateOne({"id": t["id"]}, {"$set": t}, upsert=True)
    for t in serialized_teams
]
if bulk_teams:
    teams_collection.bulk_write(bulk_teams)
    print(f"Migrati {len(bulk_teams)} team su MongoDB.")

# MIGRAZIONE LEGHE
leagues = League.objects.all()
serialized_leagues = [serialize_league(l) for l in leagues]
bulk_leagues = [
    UpdateOne({"id": l["id"]}, {"$set": l}, upsert=True)
    for l in serialized_leagues
]
if bulk_leagues:
    leagues_collection.bulk_write(bulk_leagues)
    print(f"Migrati {len(bulk_leagues)} leghe su MongoDB.")
