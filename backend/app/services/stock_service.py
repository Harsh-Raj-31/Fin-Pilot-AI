from app.schemas.stock import StockResponse


class StockService:

    def get_all_stocks(
        self,
        exchange: str | None = None,
        sector: str | None = None,
    ) -> list[StockResponse]:

        stocks = [

            StockResponse(
                symbol="RELIANCE",
                company_name="Reliance Industries Ltd.",
                exchange="NSE",
                current_price=1520.45,
                currency="INR",
                sector="Energy",
            ),

            StockResponse(
                symbol="TCS",
                company_name="Tata Consultancy Services",
                exchange="NSE",
                current_price=3875.30,
                currency="INR",
                sector="Information Technology",
            ),

            StockResponse(
                symbol="INFY",
                company_name="Infosys Limited",
                exchange="NSE",
                current_price=1658.90,
                currency="INR",
                sector="Information Technology",
            ),
        ]

        if exchange:
            stocks = [
                stock
                for stock in stocks
                if stock.exchange.upper() == exchange.upper()
            ]

        if sector:
            stocks = [
                stock
                for stock in stocks
                if stock.sector.upper() == sector.upper()
            ]

        return stocks

    def get_stock_by_symbol(self, symbol: str) -> StockResponse | None:
        stocks = self.get_all_stocks()

        for stock in stocks:
            if stock.symbol.upper() == symbol.upper():
                return stock

        return None


stock_service = StockService()