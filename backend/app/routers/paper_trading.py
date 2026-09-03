from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user

from app.schemas.paper_trading import (
    PaperAccountResponse,
    PaperPortfolioResponse,
    PaperPositionResponse,
    PaperTradeRequest,
    PaperTradeResponse,
)

from app.services.market_data_service import MarketDataService

from app.services.paper_trading_service import (
    paper_trading_service,
)


router = APIRouter(
    prefix="/paper-trading",
    tags=["Paper Trading"],
)
market_data_service = MarketDataService()


@router.get(
    "/account",
    response_model=PaperAccountResponse,
)
def get_account(
    current_user: dict = Depends(
        get_current_user
    ),
):

    user_id = current_user["id"]

    account = (
        paper_trading_service
        .get_or_create_account(user_id)
    )

    portfolio = (
        paper_trading_service
        .get_portfolio(user_id)
    )

    return {
        "user_id": user_id,
        "starting_balance": account[
            "starting_balance"
        ],
        "cash_balance": account[
            "cash_balance"
        ],
        "invested_value": portfolio[
            "invested_value"
        ],
        "current_value": portfolio[
            "current_value"
        ],
        "total_profit_loss": portfolio[
            "total_profit_loss"
        ],
        "total_return_percentage": portfolio[
            "total_return_percentage"
        ],
    }


@router.post(
    "/buy",
    status_code=status.HTTP_201_CREATED,
)
def buy_stock(
    trade: PaperTradeRequest,
    current_user: dict = Depends(
        get_current_user
    ),
):

    return paper_trading_service.buy(
        current_user["id"],
        trade.symbol,
        trade.quantity,
    )


@router.post(
    "/sell",
    status_code=status.HTTP_201_CREATED,
)
def sell_stock(
    trade: PaperTradeRequest,
    current_user: dict = Depends(
        get_current_user
    ),
):

    return paper_trading_service.sell(
        current_user["id"],
        trade.symbol,
        trade.quantity,
    )


@router.get(
    "/positions",
    response_model=list[PaperPositionResponse],
)
def get_positions(
    current_user: dict = Depends(
        get_current_user
    ),
):

    return paper_trading_service.get_positions(
        current_user["id"]
    )


@router.get(
    "/portfolio",
    response_model=PaperPortfolioResponse,
)
def get_portfolio(
    current_user: dict = Depends(
        get_current_user
    ),
):

    return paper_trading_service.get_portfolio(
        current_user["id"]
    )


@router.get(
    "/trades",
    response_model=list[PaperTradeResponse],
)
def get_trades(
    current_user: dict = Depends(
        get_current_user
    ),
):

    return paper_trading_service.get_trades(
        current_user["id"]
    )

@router.get(
    "/market-status",
)
def get_market_status(
    current_user: dict = Depends(
        get_current_user
    ),
):

    return market_data_service.get_market_status()