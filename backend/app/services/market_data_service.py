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