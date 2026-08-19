import pandas as pd
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

    def _calculate_moving_averages(self, df):
        """
        Calculate 20-period SMA and EMA.
        """

        sma_20 = df["Close"].rolling(
            window=20
        ).mean()

        ema_20 = df["Close"].ewm(
            span=20,
            adjust=False,
        ).mean()

        return (
            sma_20.iloc[-1],
            ema_20.iloc[-1],
        )   


    def _calculate_rsi(
        self,
        df,
        period: int = 14,
    ):
        """
        Calculate the Relative Strength Index (RSI).
        """

        delta = df["Close"].diff()

        gains = delta.clip(lower=0)
        losses = -delta.clip(upper=0)

        average_gain = gains.rolling(
            window=period
        ).mean()

        average_loss = losses.rolling(
            window=period
        ).mean()

        rs = average_gain / average_loss

        rsi = 100 - (
            100 / (1 + rs)
        )

        return rsi.iloc[-1] 
  

    def _calculate_macd(self, df):
        """
        Calculate MACD and MACD signal line.
        """

        ema_12 = df["Close"].ewm(
            span=12,
            adjust=False,
        ).mean()

        ema_26 = df["Close"].ewm(
            span=26,
            adjust=False,
        ).mean()

        macd = ema_12 - ema_26

        signal = macd.ewm(
            span=9,
            adjust=False,
        ).mean()

        return (
            macd.iloc[-1],
            signal.iloc[-1],
        )


    def _calculate_volatility(self, df):
        """
        Calculate historical daily price volatility.
        """

        returns = df["Close"].pct_change()

        volatility = returns.std()

        return volatility * 100


    def _safe_round(
        self,
        value,
        decimals: int = 2,
    ):
        """
        Safely round indicator values.
        Returns None when the value is NaN.
        """

        if pd.isna(value):
            return None

        return round(
            float(value),
            decimals,
        )    


    def get_stock_indicators(
        self,
        symbol: str,
        period: str = "3mo",
    ) -> dict:
        """
        Calculate technical indicators for a stock.
        """

        try:
            symbol = symbol.strip().upper()

            ticker = yf.Ticker(
                f"{symbol}.NS"
            )

            history = ticker.history(
                period=period
            )

            if history.empty:
                raise ValueError(
                    f"No market data found for {symbol}"
                )

            sma_20, ema_20 = (
                self._calculate_moving_averages(
                    history
                )
            )

            rsi_14 = self._calculate_rsi(
                history
            )

            macd, macd_signal = (
                self._calculate_macd(
                    history
                )
            )

            volatility = (
                self._calculate_volatility(
                    history
                )
            )

            return {
                "symbol": symbol,
                "period": period,
                "sma_20": self._safe_round(
                    sma_20
                ),
                "ema_20": self._safe_round(
                    ema_20
                ),
                "rsi_14": self._safe_round(
                    rsi_14
                ),
                "macd": self._safe_round(
                    macd
                ),
                "macd_signal": self._safe_round(
                    macd_signal
                ),
                "volatility": self._safe_round(
                    volatility
                ),
            }

        except Exception as e:
            raise RuntimeError(
                f"Failed to calculate indicators "
                f"for {symbol}: {e}"
            ) from e    


    


            

                    