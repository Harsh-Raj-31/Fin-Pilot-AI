from app.repositories.watchlist_repository import (
    watchlist_repository,
)
from app.services.stock_service import stock_service


class WatchlistService:

    def add_stock(
        self,
        user_id: str,
        symbol: str,
    ) -> dict:
        """
        Add a stock to the user's watchlist.
        """

        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError(
                "Stock symbol cannot be empty."
            )

        # Verify that the stock exists
        # and market data can be retrieved.
        stock = stock_service.get_stock_analysis(
            symbol
        )

        if not stock:
            raise ValueError(
                f"Stock '{symbol}' could not be found."
            )

        # Prevent duplicate watchlist entries.
        if watchlist_repository.is_stock_watched(
            user_id,
            symbol,
        ):
            raise ValueError(
                f"{symbol} is already in your watchlist."
            )

        return watchlist_repository.add_stock(
            user_id,
            symbol,
        )

    def get_watchlist(
        self,
        user_id: str,
    ) -> list[dict]:
        """
        Return the user's watchlist with
        current market information.
        """

        watchlist = (
            watchlist_repository.get_watchlist(
                user_id
            )
        )

        result = []

        for item in watchlist:
            symbol = item["symbol"]

            try:
                stock = (
                    stock_service.get_stock_analysis(
                        symbol
                    )
                )

                signal = (
                    stock_service.get_stock_signal(
                        symbol
                    )
                )

                current_price = float(
                    stock.current_price
                )

                previous_close = (
                    stock.previous_close
                )

                daily_change = 0.0

                if (
                    previous_close is not None
                    and previous_close > 0
                ):
                    daily_change = (
                        (
                            current_price
                            - previous_close
                        )
                        / previous_close
                    ) * 100

                result.append(
                    {
                        "symbol": symbol,
                        "company_name": (
                            stock.company_name
                        ),
                        "current_price": (
                            current_price
                        ),
                        "daily_change": round(
                            daily_change,
                            2,
                        ),
                        "signal": signal["signal"],
                        "confidence": signal["confidence"],
                    }
                )

            except Exception as e:
                result.append( 

                    {
                        "symbol": symbol,
                        "company_name": symbol,
                        "current_price": None,
                        "daily_change": None,
                        "signal": None,
                        "confidence": None,
                    }
                )

        return result

    def remove_stock(
        self,
        user_id: str,
        symbol: str,
    ) -> bool:
        """
        Remove a stock from the user's watchlist.
        """

        symbol = symbol.strip().upper()

        if not symbol:
            raise ValueError(
                "Stock symbol cannot be empty."
            )

        removed = (
            watchlist_repository.remove_stock(
                user_id,
                symbol,
            )
        )

        if not removed:
            raise ValueError(
                f"{symbol} is not in your watchlist."
            )

        return True


watchlist_service = WatchlistService()