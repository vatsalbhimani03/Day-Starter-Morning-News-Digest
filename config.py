import os
from datetime import datetime
from pymongo import MongoClient
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# MongoDB Configuration
MONGODB_CONN = os.getenv("MONGODB_CONNECTION_STRING", "").strip()
DBNAME = os.getenv("MONGODB_DBNAME", "daystarter").strip()

# News API Configuration
NEWS_API = os.getenv("NEWS_API_KEY", "").strip()
 
# SendGrid Email Configuration
SENDGRID_API = os.getenv("SENDGRID_API_KEY", "").strip()
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "").strip()

SEND_HOUR_LOCAL = int(os.getenv("SEND_HOUR_LOCAL", "7"))
DEFAULT_TOPICS  = [t.strip() for t in os.getenv("DEFAULT_TOPICS", "tech,world").split(",") if t.strip()]
TIMEZONE = os.getenv("TIMEZONE", "America/Toronto")