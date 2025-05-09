from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)

# Nome del database e della collezione
db = client["football_db"]
matches_collection = db["matches"]

# Funzione per creare gli indici
def create_indexes():
    # Indice su "date"
    matches_collection.create_index([("date", 1)])  # Ordine crescente

    # Indice combinato su "home_team", "away_team" e "league"
    matches_collection.create_index([("home_team", 1), ("away_team", 1), ("league", 1)])

    # Indici per i singoli team
    matches_collection.create_index([("home_team", 1)])
    matches_collection.create_index([("away_team", 1)])

    # Indice per la lega
    matches_collection.create_index([("league", 1)])

    # Puoi aggiungere altri indici se necessario
    print("Indexes created successfully.")

# Creazione degli indici all'avvio
create_indexes()
