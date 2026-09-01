from datetime import datetime, timezone

from app.database.mongodb import database


class PaperTradingRepository:

    def __init__(self):
        self.accounts = database["paper_accounts"]
        self.positions = database["paper_positions"]
        self.trades = database["paper_trades"]

    # -------------------------
    # ACCOUNT
    # -------------------------

    def get_account(self, user_id: str) -> dict | None:
        return self.accounts.find_one(
            {"user_id": user_id},
            {"_id": 0},
        )

    def create_account(
        self,
        user_id: str,
        starting_balance: float,
    ) -> dict:

        account = {
            "user_id": user_id,
            "starting_balance": starting_balance,
            "cash_balance": starting_balance,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }

        self.accounts.insert_one(account)

        return self.accounts.find_one(
            {"user_id": user_id},
            {"_id": 0},
        )

    def update_cash_balance(
        self,
        user_id: str,
        cash_balance: float,
    ) -> dict | None:

        result = self.accounts.find_one_and_update(
            {"user_id": user_id},
            {
                "$set": {
                    "cash_balance": cash_balance,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
            return_document=True,
        )

        return result

    # -------------------------
    # POSITIONS
    # -------------------------

    def get_position(
        self,
        user_id: str,
        symbol: str,
    ) -> dict | None:

        return self.positions.find_one(
            {
                "user_id": user_id,
                "symbol": symbol.upper(),
            },
            {"_id": 0},
        )

    def get_positions(self, user_id: str) -> list[dict]:

        return list(
            self.positions.find(
                {"user_id": user_id},
                {"_id": 0},
            )
        )

    def create_position(self, position: dict) -> dict:

        self.positions.insert_one(position)

        return self.positions.find_one(
            {
                "user_id": position["user_id"],
                "symbol": position["symbol"],
            },
            {"_id": 0},
        )

    def update_position(
        self,
        user_id: str,
        symbol: str,
        position_data: dict,
    ) -> dict | None:

        return self.positions.find_one_and_update(
            {
                "user_id": user_id,
                "symbol": symbol.upper(),
            },
            {
                "$set": position_data,
            },
            return_document=True,
        )

    def delete_position(
        self,
        user_id: str,
        symbol: str,
    ) -> bool:

        result = self.positions.delete_one(
            {
                "user_id": user_id,
                "symbol": symbol.upper(),
            }
        )

        return result.deleted_count > 0

    # -------------------------
    # TRADES
    # -------------------------

    def create_trade(self, trade: dict) -> dict:

        result = self.trades.insert_one(trade)

        created_trade = self.trades.find_one(
            {"_id": result.inserted_id}
        )

        created_trade["id"] = str(
            created_trade["_id"]
        )

        del created_trade["_id"]

        return created_trade

    def get_trades(
        self,
        user_id: str,
    ) -> list[dict]:

        trades = self.trades.find(
            {"user_id": user_id}
        ).sort(
            "created_at",
            -1,
        )

        result = []

        for trade in trades:

            trade["id"] = str(
                trade["_id"]
            )

            del trade["_id"]

            result.append(trade)

        return result


paper_trading_repository = PaperTradingRepository()