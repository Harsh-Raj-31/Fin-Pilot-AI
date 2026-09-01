from pymongo import MongoClient, ASCENDING

from app.config import settings


client = MongoClient(settings.MONGODB_URL)

database = client[settings.DATABASE_NAME]

database["stocks"].create_index(
    [("symbol", ASCENDING)],
    unique=True,
)

database["users"].create_index(
    [("email", ASCENDING)],
    unique=True,
)

database["portfolios"].create_index(
    [("user_id", ASCENDING)],
)
database["paper_accounts"].create_index(
    [("user_id", ASCENDING)],
    unique=True,
)

database["paper_positions"].create_index(
    [
        ("user_id", ASCENDING),
        ("symbol", ASCENDING),
    ],
    unique=True,
)

database["paper_trades"].create_index(
    [
        ("user_id", ASCENDING),
        ("created_at", -1),
    ],
)