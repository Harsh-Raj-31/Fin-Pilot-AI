from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioResponse,
    PortfolioUpdate,
)
from app.services.portfolio_service import PortfolioService


router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"],
)

portfolio_service = PortfolioService()


@router.post(
    "",
    response_model=PortfolioResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_portfolio(
    portfolio: PortfolioCreate,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["id"]

    return portfolio_service.create_portfolio(
        portfolio,
        user_id,
    )


@router.get(
    "",
    response_model=list[PortfolioResponse],
)
def get_my_portfolio(
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["id"]

    return portfolio_service.get_user_portfolios(user_id)

@router.put(
    "/{portfolio_id}",
    response_model=PortfolioResponse,
)
def update_portfolio(
    portfolio_id: str,
    portfolio: PortfolioUpdate,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["id"]

    updated_portfolio = portfolio_service.update_portfolio(
        portfolio_id,
        portfolio,
        user_id,
    )

    if updated_portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    return updated_portfolio

@router.delete(
    "/{portfolio_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_portfolio(
    portfolio_id: str,
    current_user: dict = Depends(get_current_user),
):
    user_id = current_user["id"]

    deleted = portfolio_service.delete_portfolio(
        portfolio_id,
        user_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )

    return None
