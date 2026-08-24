from app.services.market_data_service import (
    MarketDataService,
)


class StockTool:

    def __init__(self):
        self.market_data_service = (
            MarketDataService()
        )

    def get_stock_price(
        self,
        symbol: str,
    ) -> dict:

        symbol = symbol.strip().upper()

        current_price = (
            self.market_data_service
            .get_current_price(symbol)
        )

        return {
            "symbol": symbol,
            "current_price": current_price,
        }

    def get_stock_analysis(
        self,
        symbol: str,
    ) -> dict:

        symbol = symbol.strip().upper()

        market_data = (
            self.market_data_service
            .get_stock_market_data(symbol)
        )

        performance = (
            self.market_data_service
            .get_stock_performance(symbol)
        )

        risk = (
            self.market_data_service
            .get_stock_risk(symbol)
        )

        return {
            "market_data": market_data,
            "performance": performance,
            "risk": risk,
        }