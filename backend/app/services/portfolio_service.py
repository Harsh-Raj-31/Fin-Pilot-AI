from app.repositories.portfolio_repository import PortfolioRepository
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate


class PortfolioService:

    def __init__(self):
        self.portfolio_repository = PortfolioRepository()

    def create_portfolio(
        self,
        portfolio: PortfolioCreate,
        user_id: str,
    ) -> dict:

        portfolio_data = {
            "user_id": user_id,
            "symbol": portfolio.symbol.upper(),
            "quantity": portfolio.quantity,
            "average_price": portfolio.average_price,
        }

        return self.portfolio_repository.create(portfolio_data)

    def get_user_portfolios(self, user_id: str) -> list[dict]:
        return self.portfolio_repository.get_by_user_id(user_id)

    def update_portfolio(
        self,
        portfolio_id: str,
        portfolio: PortfolioUpdate,
        user_id: str,
    ) -> dict | None:

        portfolio_data = {
            "quantity": portfolio.quantity,
            "average_price": portfolio.average_price,
        }

        return self.portfolio_repository.update(
            portfolio_id,
            user_id,
            portfolio_data,
        )

    def delete_portfolio(
       self,
       portfolio_id: str,
       user_id: str,
       ) -> bool:

           return self.portfolio_repository.delete(
               portfolio_id,
               user_id,
           )