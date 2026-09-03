from app.schemas.stock import (
    StockResponse,
    StockCreate,
    StockUpdate,
)
from app.repositories.stock_repository import stock_repository
from app.core.exceptions import (
    StockAlreadyExistsException,
    StockNotFoundException,
)
from app.core.logger import logger
from app.services.market_data_service import MarketDataService
from app.services.signal_engine import signal_engine

class StockService:


    def __init__(self):
        self.market_data_service = MarketDataService()


    def _get_or_discover_stock(
        self,
        symbol: str,
    ) -> dict:

        symbol = symbol.strip().upper()

        # Step 1: Check MongoDB first

        stock = stock_repository.get_stock_by_symbol(
            symbol
        )

        if stock is not None:
            return stock

        # Step 2: Stock is not in MongoDB.
        # Try to discover it from market data.

        try:
            market_data = (
                self.market_data_service
                .get_stock_market_data(symbol)
            )

        except Exception as e:
            logger.warning(
                f"Unable to discover stock {symbol}: {e}"
            )
            raise StockNotFoundException(symbol)

        if not market_data:
            logger.warning(
                f"Stock {symbol} could not be discovered"
            )
            raise StockNotFoundException(symbol)

        # Step 3: Build the stock document

        stock_data = {
        "symbol": symbol,
        "company_name": market_data.get(
            "company_name",
            symbol,
        ),
        "exchange": market_data.get(
            "exchange",
            "NSE",
        ),
        "current_price": market_data.get(
            "current_price"
        ),
        "currency": "INR",
        "sector": market_data.get(
            "sector",
            "Unknown",
        ),
        "previous_close": market_data.get(
            "previous_close"
        ),
        "day_high": market_data.get(
            "day_high"
        ),
        "day_low": market_data.get(
            "day_low"
        ),
        "volume": market_data.get(
            "volume"
        ),
    }        

        # Step 4: Save discovered stock

        try:

            created_stock = (
                stock_repository.create_stock(
                    stock_data
                )
            )

            logger.info(
                f"Stock {symbol} discovered "
                f"and added to database"
            )

            return created_stock

        except Exception as e:

            logger.error(
                f"Failed to save discovered stock "
                f"{symbol}: {e}"
            )

            # Another request may have inserted
            # the stock at the same time.

            existing_stock = (
                stock_repository.get_stock_by_symbol(
                    symbol
                )
            )

            if existing_stock is not None:
                return existing_stock

            raise StockNotFoundException(symbol)      


    def get_all_stocks(
    self,
    page: int = 1,
    limit: int = 10,
    search: str  | None =None,
    sort_by: str = "symbol",
    order: str = "asc",
    exchange: str | None = None,
    sector: str | None = None,
) -> list[StockResponse]:

     stocks = stock_repository.get_all_stocks(
     page=page,
     limit=limit,
     search=search,
     sort_by=sort_by,
     order=order,
)

     stock_responses = [
        StockResponse(**stock)
        for stock in stocks
     ]

     if exchange:
        stock_responses = [
            stock
            for stock in stock_responses
            if stock.exchange.upper() == exchange.upper()
        ]

     if sector:
           stock_responses = [
            stock
            for stock in stock_responses
            if stock.sector.upper() == sector.upper()
        ]

     return stock_responses

    def get_stock_by_symbol(
    self,
    symbol: str,
) -> StockResponse:
  
      stock = stock_repository.get_stock_by_symbol(symbol)

      if stock is None:
          logger.warning(f"Stock {symbol} not found")
          raise StockNotFoundException(symbol)

      return StockResponse(**stock)


    def get_stock_analysis(
        self,
        symbol: str,
    ) -> StockResponse:

        symbol = symbol.strip().upper()

        stock = self._get_or_discover_stock(
          symbol
        )
        market_data = self.market_data_service.get_stock_market_data(
            symbol.upper()
        )

        stock.update(
            {
              key: value
              for key, value in market_data.items()
              if value is not None
            }
        )

        return StockResponse(**stock) 


    def get_stock_history(
        self,
        symbol: str,
        period: str = "1mo",
    ) -> list[dict]:

        symbol = symbol.strip().upper()

        stock = self._get_or_discover_stock(
           symbol
     )

        return self.market_data_service.get_stock_history(
            symbol.upper(),
            period,
        )   

    def get_stock_performance(
        self,
        symbol: str,
        period: str = "1mo",
    ) -> dict:

        symbol = symbol.strip().upper()

        stock = self._get_or_discover_stock(
            symbol
        )

        return self.market_data_service.get_stock_performance(
            symbol,
            period,
        )   


    def get_stock_risk(
        self,
        symbol: str,
        period: str = "3mo",
    ) -> dict:

        symbol = symbol.strip().upper()

        stock = self._get_or_discover_stock(
            symbol
    )

        risk_data = self.market_data_service.get_stock_risk(
            symbol,
            period,
        )

        performance_data = (
            self.market_data_service.get_stock_performance(
                symbol,
                period,
            )
        )

        risk_data["return_percentage"] = (
            performance_data["return_percentage"]
        )

        return risk_data  

    def get_stock_comparison(
        self,
        symbols: list[str],
        period: str = "3mo",
    ) -> dict:

        comparison_data = []

        for symbol in symbols:

            symbol = symbol.strip().upper()

            stock = self._get_or_discover_stock(
               symbol
            )

            performance = (
                self.market_data_service.get_stock_performance(
                    symbol,
                    period,
                )
            )

            indicators = (
                self.market_data_service.get_stock_indicators(
                    symbol,
                    period,
                )
            )

            risk = (
                self.market_data_service.get_stock_risk(
                    symbol,
                    period,
                )
            )

            # Calculate individual scores

            performance_score = (
                self._calculate_performance_score(
                    performance["return_percentage"]
                )
            )

            technical_score = (
                self._calculate_technical_score(
                    indicators["rsi_14"]
                )
            )

            risk_strength_score = (
                self._calculate_risk_strength_score(
                    risk["risk_score"]
                )
            )

            # Calculate overall comparison score

            comparison_score = (
                self._calculate_comparison_score(
                    performance_score,
                    technical_score,
                    risk_strength_score,
                )
            )

            comparison_data.append(
                {
                    "symbol": symbol,
                    "return_percentage": (
                        performance["return_percentage"]
                    ),
                    "rsi_14": indicators["rsi_14"],
                    "volatility": risk["volatility"],
                    "maximum_drawdown": (
                        risk["maximum_drawdown"]
                    ),
                    "risk_score": risk["risk_score"],
                    "risk_level": risk["risk_level"],
                    "comparison_score": comparison_score,
                }
            )

        winner = self._get_comparison_winner(
            comparison_data
        )

        return {
            "period": period,
            "stocks": comparison_data,
            "winner": winner,
        }  

    def get_stock_score(
        self,
        symbol: str,
        period: str = "3mo",
    ) -> dict:

        performance = self.market_data_service.get_stock_performance(
            symbol,
            period,
        )

        indicators = self.market_data_service.get_stock_indicators(
            symbol,
            period,
        )

        risk = self.market_data_service.get_stock_risk(
            symbol,
            period,
        )

        performance_score = signal_engine.calculate_performance_score(
            performance.get("return_percentage")
        )

        technical_score = signal_engine.calculate_technical_score(
            rsi=indicators.get("rsi_14"),
            current_price=performance.get("current_price"),
            sma_20=indicators.get("sma_20"),
            ema_20=indicators.get("ema_20"),
            macd=indicators.get("macd"),
            macd_signal=indicators.get("macd_signal"),
        )

        risk_strength_score = signal_engine.calculate_risk_strength_score(
            risk.get("risk_score")
        )

        overall_score = signal_engine.calculate_overall_score(
            performance_score,
            technical_score,
            risk_strength_score,
        )

        strength = self._get_stock_strength(
            overall_score
        )

        return {
            "symbol": symbol.upper(),
            "period": period,
            "performance_score": performance_score,
            "technical_score": technical_score,
            "risk_score": risk.get("risk_score"),
            "overall_score": overall_score,
            "strength": strength,
        }


    def get_stock_signal(
        self,
        symbol: str,
        period: str = "3mo",
    ) -> dict:

        score_data = self.get_stock_score(
            symbol,
            period,
        )

        market_data = self.get_market_condition(
            period
        )

        signal = signal_engine.determine_signal(
            score_data.get("overall_score"),
            market_data.get("trend", "NEUTRAL"),
        )

        confidence = signal_engine.calculate_confidence(
            score_data.get("overall_score"),
            market_data.get("market_strength"),
            market_data.get("trend", "NEUTRAL"),
        )

        return {
            "symbol": symbol.upper(),
            "period": period,
            "stock_score": score_data.get(
                "overall_score"
            ),
            "market_trend": market_data.get(
                "trend"
            ),
            "market_strength": market_data.get(
                "market_strength"
            ),
            "signal": signal,
            "confidence": confidence,
        }

    def get_market_condition(
        self,
        period: str = "3mo",
    ) -> dict:

        history = (
            self.market_data_service.get_market_history(
                period
            )
        )

        if not history:
            raise ValueError(
                "No market data available for NIFTY 50"
            )

        closes = [
            item["close"]
            for item in history
        ]

        current_price = closes[-1]

        start_price = closes[0]

        return_percentage = (
            (current_price - start_price)
            / start_price
        ) * 100

        # Calculate 20-period SMA

        if len(closes) >= 20:
            sma_20 = (
                sum(closes[-20:])
                / 20
            )
        else:
            sma_20 = None

        # Calculate 20-period EMA

        if len(closes) >= 20:

            multiplier = 2 / (20 + 1)

            ema_20 = closes[0]

            for price in closes[1:]:

                ema_20 = (
                    (price - ema_20)
                    * multiplier
                    + ema_20
                )

        else:
            ema_20 = None

        trend = self._get_market_trend(
          current_price,
          sma_20,
          ema_20,
          return_percentage,
        )

        market_strength = (
            self._calculate_market_strength(
                current_price,
                sma_20,
                ema_20,
                return_percentage,
            )
        )
            
        return {
            "market": "NIFTY 50",
            "period": period,
            "current_price": round(
                current_price,
                2,
            ),
            "sma_20": (
                round(sma_20, 2)
                if sma_20 is not None
                else None
            ),
            "ema_20": (
                round(ema_20, 2)
                if ema_20 is not None
                else None
            ),
            "return_percentage": round(
                return_percentage,
                2,
            ),
            "trend": trend,
            "market_strength": market_strength,
        }    


    def _get_market_trend(
        self,
        current_price,
        sma_20,
        ema_20,
        return_percentage,
    ):
        """
        Determine the overall market trend.
        """

        if (
            current_price is None
            or sma_20 is None
            or ema_20 is None
            or return_percentage is None
        ):
            return "NEUTRAL"

        if (
            current_price > sma_20
            and current_price > ema_20
            and return_percentage > 0
        ):
            return "BULLISH"

        if (
            current_price < sma_20
            and current_price < ema_20
            and return_percentage < 0
        ):
            return "BEARISH"

        return "NEUTRAL" 


    def _calculate_market_strength(
        self,
        current_price,
        sma_20,
        ema_20,
        return_percentage,
    ):
        """
        Calculate market strength from 0 to 100.
        """

        if (
            current_price is None
            or sma_20 is None
            or ema_20 is None
            or return_percentage is None
        ):
            return None

        # Price vs SMA score

        if current_price > sma_20:
            sma_score = 100
        else:
            sma_score = 0

        # Price vs EMA score

        if current_price > ema_20:
            ema_score = 100
        else:
            ema_score = 0

        # Return score

        if return_percentage >= 5:
            return_score = 100
        elif return_percentage >= 0:
            return_score = 60
        else:
            return_score = 30

        market_strength = (
            sma_score * 0.40
            + ema_score * 0.30
            + return_score * 0.30
        )

        return round(
            market_strength,
            2,
        )       

    
    def _get_stock_strength(
        self,
        overall_score,
    ):
        """
        Convert the overall stock score
        into a strength classification.
        """

        if overall_score is None:
            return "UNKNOWN"

        if overall_score <= 30:
            return "WEAK"

        if overall_score <= 60:
            return "NEUTRAL"

        if overall_score <= 80:
            return "STRONG"

        return "VERY STRONG"  


    def _get_stock_signal(
        self,
        stock_score,
        market_trend,
    ):
        """
        Determine the stock decision signal
        using stock score and market trend.
        """

        if stock_score is None:
            return "HOLD"

        # Strong stock + bullish market
        if (
            stock_score >= 70
            and market_trend == "BULLISH"
        ):
            return "BUY"

        # Weak stock + bearish market
        if (
            stock_score < 40
            and market_trend == "BEARISH"
        ):
            return "AVOID"

        # Strong stock but market confirmation is missing
        if stock_score >= 60:
            return "WATCH"

        # Default condition
        return "HOLD"


    def get_stock_explanation(
        self,
        symbol: str,
        period: str = "3mo",
    ) -> dict:

        symbol = symbol.strip().upper()

        stock = self._get_or_discover_stock(
           symbol
        )
        # Get complete signal data

        signal_data = (
            self.get_stock_signal(
                symbol,
                period,
            )
        )

        stock_score = (
            signal_data["stock_score"]
        )

        market_trend = (
            signal_data["market_trend"]
        )

        market_strength = (
            signal_data["market_strength"]
        )

        signal = signal_data["signal"]

        confidence = (
            signal_data["confidence"]
        )

        # Generate reasons

        reasons = self._get_signal_reasons(
            stock_score,
            market_trend,
            market_strength,
            signal,
        )

        # Generate summary

        summary = self._get_signal_summary(
            symbol,
            signal,
            stock_score,
            market_trend,
        )

        return {
            "symbol": symbol,
            "period": period,
            "signal": signal,
            "confidence": confidence,
            "summary": summary,
            "reasons": reasons,
        }    


    def _calculate_signal_confidence(
        self,
        stock_score,
        market_strength,
        market_trend,
    ):
        """
        Calculate signal confidence from 0 to 100.
        """

        if (
            stock_score is None
            or market_strength is None
        ):
            return None

        if market_trend == "BULLISH":
            market_alignment = 100

        elif market_trend == "NEUTRAL":
            market_alignment = 60

        else:
            market_alignment = 30

        confidence = (
            stock_score * 0.50
            + market_strength * 0.30
            + market_alignment * 0.20
        )

        return round(
            confidence,
            2,
        )  


    def _get_signal_reasons(
        self,
        stock_score,
        market_trend,
        market_strength,
        signal,
    ) -> list[str]:
        """
        Generate rule-based reasons for the stock signal.
        """

        reasons = []

        # Stock score explanation

        if stock_score is None:
            reasons.append(
                "Stock score could not be calculated."
            )

        elif stock_score >= 80:
            reasons.append(
                "The stock has a very strong overall score."
            )

        elif stock_score >= 60:
            reasons.append(
                "The stock has a strong overall score."
            )

        elif stock_score >= 40:
            reasons.append(
                "The stock has a moderate overall score."
            )

        else:
            reasons.append(
                "The stock has a weak overall score."
            )

        # Market trend explanation

        if market_trend == "BULLISH":
            reasons.append(
                "The broader market trend is bullish."
            )

        elif market_trend == "BEARISH":
            reasons.append(
                "The broader market trend is bearish."
            )

        else:
            reasons.append(
                "The broader market trend is neutral."
            )

        # Market strength explanation

        if market_strength is None:
            reasons.append(
                "Market strength could not be calculated."
            )

        elif market_strength >= 70:
            reasons.append(
                "The market is showing strong momentum."
            )

        elif market_strength >= 40:
            reasons.append(
                "The market is showing moderate strength."
            )

        else:
            reasons.append(
                "The market is showing weak strength."
            )

        # Signal-specific explanation

        if signal == "BUY":
            reasons.append(
                "The stock score and market conditions "
                "provide confirmation for a BUY signal."
            )

        elif signal == "WATCH":
            reasons.append(
                "The stock shows potential, but market "
                "conditions do not provide enough confirmation "
                "for a BUY signal."
            )

        elif signal == "AVOID":
            reasons.append(
                "Both the stock and broader market conditions "
                "are weak."
            )

        else:
            reasons.append(
                "The current conditions do not provide "
                "a strong enough setup for BUY or AVOID."
            )

        return reasons   


    def _get_signal_summary(
        self,
        symbol: str,
        signal: str,
        stock_score,
        market_trend: str,
    ) -> str:
        """
        Generate a short summary explaining
        the current stock signal.
        """

        if signal == "BUY":
            return (
                f"{symbol} currently has a BUY signal "
                f"because the stock score is strong and "
                f"the broader market trend is bullish."
            )

        if signal == "WATCH":
            return (
                f"{symbol} currently has a WATCH signal "
                f"because the stock shows potential, "
                f"but the broader market does not provide "
                f"enough confirmation for a BUY signal."
            )

        if signal == "AVOID":
            return (
                f"{symbol} currently has an AVOID signal "
                f"because the stock score is weak and "
                f"the broader market trend is bearish."
            )

        return (
            f"{symbol} currently has a HOLD signal "
            f"because the stock score and market conditions "
            f"do not provide a strong enough setup for "
            f"BUY or AVOID."
        )                 


    def _calculate_comparison_score(
        self,
        performance_score,
        technical_score,
        risk_strength_score,
    ):
        """
        Calculate the overall comparison score.

        Performance: 40%
        Technical:   30%
        Risk:        30%
        """

        if (
            performance_score is None
            or technical_score is None
            or risk_strength_score is None
        ):
            return None

        return (
            performance_score * 0.40
            + technical_score * 0.30
            + risk_strength_score * 0.30
        )     


    def _get_comparison_winner(
        self,
        comparison_data: list[dict],
    ) -> str | None:
        """
        Return the stock with the highest
        comparison score.
        """

        valid_stocks = [
            stock
            for stock in comparison_data
            if stock["comparison_score"] is not None
        ]

        if not valid_stocks:
            return None

        winner = max(
            valid_stocks,
            key=lambda stock: stock["comparison_score"],
        )

        return winner["symbol"]              


    def get_stock_indicators(
        self,
        symbol: str,
        period: str = "3mo",
    ) -> dict:

        symbol = symbol.strip().upper()

        stock = self._get_or_discover_stock(
             symbol
        )

        return self.market_data_service.get_stock_indicators(
            symbol,
            period,
        )    


    def create_stock(self, stock: StockCreate) -> StockResponse:
        """
        Creates a new stock after checking for duplicates.
        """

        existing_stock = stock_repository.get_stock_by_symbol(stock.symbol)

        if existing_stock:
            logger.warning(f"Stock {stock.symbol} already exists")
            raise StockAlreadyExistsException(stock.symbol)
            
        created_stock = stock_repository.create_stock(
            stock.model_dump()
        )
        logger.info(f"Stock {stock.symbol} created successfully")

        return StockResponse(**created_stock)  
         
    def update_stock(self,symbol: str,stock: StockUpdate,) -> StockResponse:
        """
        Updates a stock by its symbol.
        """

        updated_stock = stock_repository.update_stock(
            symbol=symbol,
            stock=stock.model_dump(),
        )

        if updated_stock is None:
            logger.warning(f"Stock {symbol} not found for update")
            raise StockNotFoundException(symbol)

        logger.info(f"Stock {symbol} updated successfully")

        return StockResponse(**updated_stock) 
    
    def delete_stock(self, symbol: str) -> None:
        """
        Deletes a stock by its symbol.
        """

        deleted = stock_repository.delete_stock(symbol)

        if not deleted:
            logger.warning(f"Stock {symbol} not found for deletion")
            raise StockNotFoundException(symbol) 

        logger.info(f"Stock {symbol} deleted successfully")        

stock_service = StockService()