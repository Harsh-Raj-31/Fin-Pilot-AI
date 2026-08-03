from app.repositories.stock_repository import stock_repository
from app.schemas.stock import StockResponse



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


stock_service = StockService()