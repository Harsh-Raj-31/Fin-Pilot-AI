from app.schemas.stock import (
    StockResponse,
    StockCreate,
    StockUpdate,
)

from app.repositories.stock_repository import stock_repository
from app.core.exceptions import StockNotFoundException


class StockService:

    def get_all_stocks(
    self,
    exchange: str | None = None,
    sector: str | None = None,
) -> list[StockResponse]:

     stocks = stock_repository.get_all_stocks()

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

    def get_stock_by_symbol(self, symbol: str) -> StockResponse | None:
        stocks = self.get_all_stocks()

        for stock in stocks:
            if stock.symbol.upper() == symbol.upper():
                return stock

        return None

    def create_stock(self, stock: StockCreate) -> StockResponse:
        """
        Creates a new stock after checking for duplicates.
        """

        existing_stock = stock_repository.get_stock_by_symbol(stock.symbol)

        if existing_stock:
            raise FinPilotException(
                f"Stock '{stock.symbol}' already exists."
            )

        created_stock = stock_repository.create_stock(
            stock.model_dump()
        )

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
            raise StockNotFoundException(symbol)

        return StockResponse(**updated_stock) 
    def delete_stock(self, symbol: str) -> None:
        """
        Deletes a stock by its symbol.
        """

        deleted = stock_repository.delete_stock(symbol)

        if not deleted:
            raise StockNotFoundException(symbol)         

stock_service = StockService()