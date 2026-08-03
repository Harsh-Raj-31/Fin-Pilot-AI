from pymongo import MongoClient

from app.config import settings

client = MongoClient(settings.MONGODB_URI)

database = client[settings.DATABASE_NAME]