from app.database.mongodb import database


class PortfolioRepository:

    def __init__(self):
        self.collection = database["portfolios"]

    def create(self, portfolio: dict) -> dict:
        result = self.collection.insert_one(portfolio)

        created_portfolio = self.collection.find_one(
            {"_id": result.inserted_id}
        )

        created_portfolio["id"] = str(created_portfolio["_id"])
        del created_portfolio["_id"]

        return created_portfolio

    def get_by_user_id(self, user_id: str) -> list[dict]:
       portfolios = self.collection.find(
           {"user_id": user_id}
       )

       result = []

       for portfolio in portfolios:
           portfolio["id"] = str(portfolio["_id"])
           del portfolio["_id"]
           result.append(portfolio)

       return result


    def update(
        self,
        portfolio_id: str,
        user_id: str,
        portfolio_data: dict,
    ) -> dict | None:

        from bson import ObjectId

        updated_portfolio = self.collection.find_one_and_update(
            {
                "_id": ObjectId(portfolio_id),
                "user_id": user_id,
            },
            {
                "$set": portfolio_data
            },
            return_document=True,
        )

        if updated_portfolio is None:
            return None

        updated_portfolio["id"] = str(updated_portfolio["_id"])
        del updated_portfolio["_id"]

        return updated_portfolio   


    def delete(
    self,
    portfolio_id: str,
    user_id: str,
) -> bool:

       from bson import ObjectId

       result = self.collection.delete_one(
           {
               "_id": ObjectId(portfolio_id),
               "user_id": user_id,
           }
       )

       return result.deleted_count > 0        