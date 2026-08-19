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