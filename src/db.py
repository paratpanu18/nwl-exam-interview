from pymongo import MongoClient
from src.settings import Settings

SETTINGS = Settings()

client = MongoClient(SETTINGS.MONGO_CONNECTION_STRING)
db = client[SETTINGS.MONGO_DB_NAME]

senior_collection = db["senior"]
junior_collection = db["junior"]
criteria_type_collection = db["criteria_type"]
criteria_collection = db["criteria"]
score_collection = db["score"]
