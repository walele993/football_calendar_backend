from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)

# Nome del database e della collezione
db = client["football_db"]
matches_collection = db["matches"]
