from pymongo import MongoClient
from src.settings import Settings

SETTINGS = Settings()

client = MongoClient(SETTINGS.MONGO_CONNECTION_STRING)
db = client[SETTINGS.MONGO_DB_NAME]

criteria_type_collection = db["criteria_type_collection"]
criteria_collection = db["criteria_collection"]
interviewer_collection = db["interviewers"]
participant_collection = db["participants"]
