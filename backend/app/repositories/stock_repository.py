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


    def create_stock(self, stock: dict) -> dict:
        """
        Inserts a new stock into MongoDB.
        """
        self.collection.insert_one(stock)
        return stock

    def get_stock_by_symbol(self, symbol: str) -> dict | None:
        """
        Returns a stock document by its symbol.
        """
        stock = self.collection.find_one(
            {"symbol": symbol.upper()},
            {"_id": 0},
        )
        return stock
    def update_stock(self,symbol: str,stock: dict,) -> dict | None:
         """
         Updates a stock by its symbol.
         """

         result = self.collection.update_one(
             {"symbol": symbol.upper()},
             {"$set": stock},
         )

         if result.matched_count == 0:
             return None

         return self.get_stock_by_symbol(symbol)    

    def delete_stock(self, symbol: str) -> bool:    
        """
        Deletes a stock by its symbol.
        """

        result = self.collection.delete_one(
            {"symbol": symbol.upper()}
        )

        return result.deleted_count > 0     
stock_repository = StockRepository()