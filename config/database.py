from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017")

# Database
db = client["whatsapp_bot"]

# Collections
webhooks_collection = db["webhooks"]
conversations_collection = db["conversations"]
users_collection = db["users"]
