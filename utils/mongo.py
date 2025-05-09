# utils/mongo.py
import os
from pymongo import MongoClient

client = MongoClient(os.environ["MONGODB_URI"])  # la URI verrà da Vercel
db = client["football_db"]  # nome del tuo database MongoDB
matches_collection = db["matches"]  # la "tabella" delle partite
