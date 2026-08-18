import yfinance as yf


class MarketDataService:

    def get_current_price(self, symbol: str) -> float:

        try:
            ticker = yf.Ticker(f"{symbol}.NS")

            data = ticker.history(period="1d")

            if data.empty:
                raise ValueError(
                    f"No market data found for {symbol}"
                )

            current_price = data["Close"].iloc[-1]

            if current_price is None:
                raise ValueError(
                    f"Current price unavailable for {symbol}"
                )

            return float(current_price)

        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch market data for {symbol}: {e}"
            ) from e

    def get_stock_market_data(self, symbol: str) -> dict:

        try:
            ticker = yf.Ticker(f"{symbol}.NS")

            data = ticker.history(period="5d")

            if data.empty:
                raise ValueError(
                    f"No market data found for {symbol}"
                )

            latest = data.iloc[-1]

            current_price = round(float(latest["Close"]), 2)
            day_high = round(float(latest["High"]), 2)
            day_low = round(float(latest["Low"]), 2)
            volume = int(latest["Volume"])

            if len(data) >= 2:
                previous_close = round(
                float(data.iloc[-2]["Close"]),
                2,
                )            
            else:
                previous_close = current_price

            return {
                "current_price": current_price,
                "previous_close": previous_close,
                "day_high": day_high,
                "day_low": day_low,
                "volume": volume,
            }

        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch market data for {symbol}: {e}"
            ) from e  

    def get_stock_history(
        self,
        symbol: str,
        period: str = "1mo",
    ) -> list[dict]:

        try:
            ticker = yf.Ticker(f"{symbol}.NS")

            data = ticker.history(period=period)

            if data.empty:
                raise ValueError(
                    f"No historical market data found for {symbol}"
                )

            history = []

            for date, row in data.iterrows():

                history.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"]),
                })

            return history

        except Exception as e:
            raise RuntimeError(
                f"Failed to fetch historical market data "
                f"for {symbol}: {e}"
            ) from e    

    def get_stock_performance(
        self,
        symbol: str,
        period: str = "1mo",
    ) -> dict:

        try:
            history = self.get_stock_history(
                symbol,
                period,
            )

            if not history:
                raise ValueError(
                    f"No historical market data found for {symbol}"
                )

            start_price = history[0]["close"]
            current_price = history[-1]["close"]

            highest_price = max(
                item["high"]
                for item in history
            )

            lowest_price = min(
                item["low"]
                for item in history
            )

            average_price = (
                sum(item["close"] for item in history)
                / len(history)
            )

            return_percentage = (
                (current_price - start_price)
                / start_price
            ) * 100

            return {
                "symbol": symbol.upper(),
                "period": period,
                "start_price": round(start_price, 2),
                "current_price": round(current_price, 2),
                "return_percentage": round(
                    return_percentage,
                    2,
                ),
                "highest_price": round(
                    highest_price,
                    2,
                ),
                "lowest_price": round(
                    lowest_price,
                    2,
                ),
                "average_price": round(
                    average_price,
                    2,
                ),
            }

        except Exception as e:
            raise RuntimeError(
                f"Failed to calculate performance "
                f"for {symbol}: {e}"
            ) from e              