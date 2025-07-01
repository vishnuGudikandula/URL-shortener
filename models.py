
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["logstream"]
collection = db["metrics"]

def insert_metrics(data):
    collection.insert_one(data)

def get_latest_metrics():
    return list(collection.find().sort("processed_at", -1).limit(5))
