class StockService:

    def get_all_stocks(self) -> list[dict]:
        return [
            {
                "symbol": "RELIANCE",
                "price": 1520.45,
            },
            {
                "symbol": "TCS",
                "price": 3875.30,
            },
            {
                "symbol": "INFY",
                "price": 1658.90,
            },
        ]


stock_service = StockService()