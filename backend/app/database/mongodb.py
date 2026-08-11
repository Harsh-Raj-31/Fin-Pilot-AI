from pymongo import MongoClient, ASCENDING

from app.config import settings


client = MongoClient(settings.MONGODB_URL)

database = client[settings.DATABASE_NAME]

database["stocks"].create_index(
    [("symbol", ASCENDING)],
    unique=True,
)