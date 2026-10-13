from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


MONGO_URI = os.getenv("MONGODB_URI") 


if not MONGO_URI:
  MONGO_URI = "mongodb://localhost:27017/"

# raise ValueError("MONGO_URI is not configured")  no fallback when live


client = MongoClient(MONGO_URI)

db = client["intucate_db"]


def init_db():
  try:
    client.admin.command('ping')
    print("MongoDB Connected successfully!")
  except Exception as e:
    print(f"MongoDB connection failed: {e}")


