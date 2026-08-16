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