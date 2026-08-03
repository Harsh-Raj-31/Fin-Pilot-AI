from app.database.mongodb import database


class StockRepository:
    def __init__(self):
        self.collection = database["stocks"]

    def get_all_stocks(self) -> list[dict]:
        """
        Returns all stock documents from MongoDB.
        """
        stocks = list(self.collection.find({}, {"_id": 0}))
        return stocks


stock_repository = StockRepository()