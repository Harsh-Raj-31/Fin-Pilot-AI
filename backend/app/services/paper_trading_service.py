from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories.paper_trading_repository import (
    paper_trading_repository,
)
from app.services.market_data_service import MarketDataService


STARTING_BALANCE = 100000.0


class PaperTradingService:

    def __init__(self):
        self.repository = paper_trading_repository
        self.market_data_service = MarketDataService()

    # -------------------------
    # ACCOUNT
    # -------------------------

    def get_or_create_account(
        self,
        user_id: str,
    ) -> dict:

        account = self.repository.get_account(user_id)

        if account is None:
            account = self.repository.create_account(
                user_id,
                STARTING_BALANCE,
            )

        return account

    # -------------------------
    # MARKET PRICE
    # -------------------------

    def get_current_price(
        self,
        symbol: str,
    ) -> float:

        symbol = symbol.upper()

        try:
            market_data = (
                self.market_data_service
                .get_stock_market_data(symbol)
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Unable to fetch market data "
                    f"for {symbol}"
                ),
            ) from exc

        current_price = market_data.get(
            "current_price"
        )

        if current_price is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Current price unavailable "
                    f"for {symbol}"
                ),
            )

        return float(current_price)

    # -------------------------
    # BUY
    # -------------------------

    def buy(
        self,
        user_id: str,
        symbol: str,
        quantity: float,
    ) -> dict:

        symbol = symbol.upper()

        account = self.get_or_create_account(
            user_id
        )

        current_price = self.get_current_price(
            symbol
        )

        total_value = current_price * quantity

        if account["cash_balance"] < total_value:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Insufficient virtual cash "
                    "to execute this trade."
                ),
            )

        position = self.repository.get_position(
            user_id,
            symbol,
        )

        if position:

            old_quantity = position["quantity"]
            old_average_price = position[
                "average_price"
            ]

            new_quantity = (
                old_quantity + quantity
            )

            new_average_price = (
                (
                    old_quantity
                    * old_average_price
                )
                + total_value
            ) / new_quantity

            self.repository.update_position(
                user_id,
                symbol,
                {
                    "quantity": new_quantity,
                    "average_price": new_average_price,
                    "updated_at": datetime.now(
                        timezone.utc
                    ),
                },
            )

        else:

            self.repository.create_position(
                {
                    "user_id": user_id,
                    "symbol": symbol,
                    "quantity": quantity,
                    "average_price": current_price,
                    "created_at": datetime.now(
                        timezone.utc
                    ),
                    "updated_at": datetime.now(
                        timezone.utc
                    ),
                }
            )

        new_cash_balance = (
            account["cash_balance"]
            - total_value
        )

        self.repository.update_cash_balance(
            user_id,
            new_cash_balance,
        )

        trade = self.repository.create_trade(
            {
                "user_id": user_id,
                "symbol": symbol,
                "side": "BUY",
                "quantity": quantity,
                "price": current_price,
                "total_value": total_value,
                "realized_profit_loss": 0,
                "created_at": datetime.now(
                    timezone.utc
                ),
            }
        )

        return {
            "message": "Paper BUY order executed successfully.",
            "trade": trade,
            "cash_balance": new_cash_balance,
        }

    # -------------------------
    # SELL
    # -------------------------

    def sell(
        self,
        user_id: str,
        symbol: str,
        quantity: float,
    ) -> dict:

        symbol = symbol.upper()

        account = self.get_or_create_account(
            user_id
        )

        position = self.repository.get_position(
            user_id,
            symbol,
        )

        if position is None:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"You do not own any "
                    f"{symbol} shares."
                ),
            )

        if position["quantity"] < quantity:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "You cannot sell more shares "
                    "than you currently own."
                ),
            )

        current_price = self.get_current_price(
            symbol
        )

        total_value = current_price * quantity

        # Calculate profit/loss generated by
        # the shares being sold.
        realized_profit_loss = (
            current_price
            - position["average_price"]
        ) * quantity

        remaining_quantity = (
            position["quantity"] - quantity
        )

        if remaining_quantity == 0:

            self.repository.delete_position(
                user_id,
                symbol,
            )

        else:

            self.repository.update_position(
                user_id,
                symbol,
                {
                    "quantity": remaining_quantity,
                    "updated_at": datetime.now(
                        timezone.utc
                    ),
                },
            )

        new_cash_balance = (
            account["cash_balance"]
            + total_value
        )

        self.repository.update_cash_balance(
            user_id,
            new_cash_balance,
        )

        trade = self.repository.create_trade(
            {
                "user_id": user_id,
                "symbol": symbol,
                "side": "SELL",
                "quantity": quantity,
                "price": current_price,
                "total_value": total_value,
                "realized_profit_loss": realized_profit_loss,
                "created_at": datetime.now(
                    timezone.utc
                ),
            }
        )

        return {
            "message": "Paper SELL order executed successfully.",
            "trade": trade,
            "cash_balance": new_cash_balance,
        }

    # -------------------------
    # POSITIONS
    # -------------------------

    def get_positions(
        self,
        user_id: str,
    ) -> list[dict]:

        positions = self.repository.get_positions(
            user_id
        )

        result = []

        for position in positions:

            current_price = self.get_current_price(
                position["symbol"]
            )

            quantity = position["quantity"]

            average_price = position[
                "average_price"
            ]

            invested_value = (
                quantity * average_price
            )

            current_value = (
                quantity * current_price
            )

            profit_loss = (
                current_value - invested_value
            )

            profit_loss_percentage = (
                (
                    profit_loss
                    / invested_value
                )
                * 100
                if invested_value > 0
                else 0
            )

            result.append(
                {
                    "symbol": position["symbol"],
                    "quantity": quantity,
                    "average_price": average_price,
                    "current_price": current_price,
                    "invested_value": invested_value,
                    "current_value": current_value,
                    "profit_loss": profit_loss,
                    "profit_loss_percentage": profit_loss_percentage,
                }
            )

        return result

    # -------------------------
    # PORTFOLIO
    # -------------------------

    def get_portfolio(
        self,
        user_id: str,
    ) -> dict:

        account = self.get_or_create_account(
            user_id
        )

        positions = self.get_positions(
            user_id
        )

        invested_value = sum(
            position["invested_value"]
            for position in positions
        )

        current_value = sum(
            position["current_value"]
            for position in positions
        )

        total_profit_loss = (
            current_value - invested_value
        )

        starting_balance = account[
            "starting_balance"
        ]

        total_account_value = (
            account["cash_balance"]
            + current_value
        )

        total_profit_loss_from_start = (
            total_account_value
            - starting_balance
        )

        total_return_percentage = (
            (
                total_profit_loss_from_start
                / starting_balance
            )
            * 100
            if starting_balance > 0
            else 0
        )

        # -------------------------
        # PORTFOLIO ALLOCATION
        # -------------------------

        allocation = []

        if total_account_value > 0:
            # Stock allocation
            for position in positions:

                percentage = (
                    position["current_value"]
                    / total_account_value
                ) * 100

                allocation.append(
                    {
                        "symbol": position["symbol"],
                        "value": position["current_value"],
                        "percentage": percentage,
                    }
                )

                # Cash allocation
                cash_percentage = (
                    account["cash_balance"]
                    / total_account_value
                ) * 100

                allocation.append(
                    {
                        "symbol": "Cash",
                        "value": account["cash_balance"],
                        "percentage": cash_percentage,
                    }
                )

        return {
            "cash_balance": account[
                "cash_balance"
            ],
            "invested_value": invested_value,
            "current_value": current_value,
            "total_profit_loss": total_profit_loss_from_start,
            "total_return_percentage": total_return_percentage,
            "positions": positions,
            "allocation": allocation,
        }
    # -------------------------
    # TRADE HISTORY
    # -------------------------

    def get_trades(
        self,
        user_id: str,
    ) -> list[dict]:

        return self.repository.get_trades(
            user_id
        )


paper_trading_service = PaperTradingService()