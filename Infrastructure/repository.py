from typing import Any
from pymongo import MongoClient, ASCENDING

from config import MONGODB_CONN, DBNAME
from model import Subscriber

class MongoDBRepo:
    def __init__(self):
        self.client = MongoClient(MONGODB_CONN, serverSelectionTimeoutMS=5000)
        self.db = self.client[DBNAME]
        self.subscribers = self.db["subscribers"]
        # Ensure unique index on email field
        self.subscribers.create_index([("email", ASCENDING)], unique=True)
    
    def upsert_subscriber(self, s: Subscriber) -> str:
        # Upsert subscriber in MongoDB - create or update
        doc = {
            "email": s.email,
            "topics": [t.strip().lower() for t in s.topics],
            "timezone": s.timezone,
            "send_hour": s.send_hour,
            "active": s.active,
            "verified": s.verified,
            "created_at": s.created_at,
        }
        self.subscribers.update_one({"email": s.email}, {"$set": doc}, upsert=True)
        return "Subscriber upserted/saved."
    
    def remove_subscriber(self, email: str) -> str:
        # Remove subscriber from MongoDB - soft delete (set active to False)
        self.subscribers.update_one({"email": email}, {"$set": {"active": False}})
        return "Subscriber removed/ Unsubscribed."

    def get_subscriber(self, email: str) -> Subscriber:
        # Get active subscriber from MongoDB
        return self.subscribers.find_one({"email": email, "active":True})
    
    def get_active_subscribers(self) -> list[dict[str, Any]]:
        # Get all active subscribers from MongoDB 
        return list(self.subscribers.find({"active": True}))
