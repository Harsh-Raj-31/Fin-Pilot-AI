from datetime import datetime, timezone

from app.database.mongodb import database


class WatchlistRepository:

    def __init__(self):
        self.collection = database["watchlists"]

    def add_stock(
        self,
        user_id: str,
        symbol: str,
    ) -> dict:
        """
        Add a stock to a user's watchlist.
        """

        document = {
            "user_id": user_id,
            "symbol": symbol.upper(),
            "created_at": datetime.now(timezone.utc),
        }

        self.collection.insert_one(document)

        return {
            "user_id": user_id,
            "symbol": symbol.upper(),
            "created_at": document["created_at"],
        }

    def get_watchlist(
        self,
        user_id: str,
    ) -> list[dict]:
        """
        Return all stocks in the user's watchlist.
        """

        return list(
            self.collection.find(
                {"user_id": user_id},
                {"_id": 0},
            ).sort("created_at", -1)
        )

    def is_stock_watched(
        self,
        user_id: str,
        symbol: str,
    ) -> bool:
        """
        Check whether a stock already exists
        in the user's watchlist.
        """

        stock = self.collection.find_one(
            {
                "user_id": user_id,
                "symbol": symbol.upper(),
            }
        )

        return stock is not None

    def remove_stock(
        self,
        user_id: str,
        symbol: str,
    ) -> bool:
        """
        Remove a stock from the user's watchlist.
        """

        result = self.collection.delete_one(
            {
                "user_id": user_id,
                "symbol": symbol.upper(),
            }
        )

        return result.deleted_count > 0


watchlist_repository = WatchlistRepository()