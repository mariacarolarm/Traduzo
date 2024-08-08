import os
from pymongo import MongoClient

client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017"))

db = client[os.getenv("DB_NAME", "test_db_traduzo")]
