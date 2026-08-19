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

class StockService:

    def __init__(self):
        self.market_data_service = MarketDataService()

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

        stock = stock_repository.get_stock_by_symbol(symbol)

        if stock is None:
            logger.warning(f"Stock {symbol} not found")
            raise StockNotFoundException(symbol)

        market_data = self.market_data_service.get_stock_market_data(
            symbol.upper()
        )

        stock.update(market_data)

        return StockResponse(**stock) 


    def get_stock_history(
        self,
        symbol: str,
        period: str = "1mo",
    ) -> list[dict]:

        symbol = symbol.strip().upper()

        stock = stock_repository.get_stock_by_symbol(symbol)

        if stock is None:
            logger.warning(f"Stock {symbol} not found")
            raise StockNotFoundException(symbol)

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

        stock = stock_repository.get_stock_by_symbol(symbol)

        if stock is None:
            logger.warning(f"Stock {symbol} not found")
            raise StockNotFoundException(symbol)

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

        stock = stock_repository.get_stock_by_symbol(symbol)

        if stock is None:
            logger.warning(f"Stock {symbol} not found")
            raise StockNotFoundException(symbol)

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

            stock = stock_repository.get_stock_by_symbol(
                symbol
            )

            if stock is None:
                logger.warning(
                    f"Stock {symbol} not found"
                )
                raise StockNotFoundException(symbol)

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

    
    def _calculate_performance_score(
        self,
        return_percentage,
    ):
        """
        Convert stock return into a
        0-100 performance score.
        """

        if return_percentage is None:
            return None

        if return_percentage >= 10:
            return 100

        if return_percentage >= 5:
            return 80

        if return_percentage >= 0:
            return 60

        if return_percentage >= -5:
            return 40

        if return_percentage >= -10:
            return 20

        return 0


    def _calculate_technical_score(
        self,
        rsi,
    ):
        """
        Convert RSI into a 0-100 technical score.
        """

        if rsi is None:
            return None

        if 50 <= rsi < 70:
            return 80

        if 40 <= rsi < 50:
            return 70

        if 30 <= rsi < 40:
            return 60

        if 70 <= rsi < 80:
            return 50

        if rsi < 30:
            return 40

        return 30     


    def _calculate_risk_strength_score(
        self,
        risk_score,
    ):
        """
        Convert risk score into a
        0-100 risk strength score.

        Lower risk = higher score.
        """

        if risk_score is None:
            return None

        return 100 - risk_score


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

        stock = stock_repository.get_stock_by_symbol(symbol)

        if stock is None:
            logger.warning(f"Stock {symbol} not found")
            raise StockNotFoundException(symbol)

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