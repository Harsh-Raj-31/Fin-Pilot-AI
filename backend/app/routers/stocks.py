from fastapi import APIRouter, Path, Query, status

from app.core.exceptions import StockNotFoundException
from app.schemas.stock import StockResponse
from app.services.stock_service import stock_service

router = APIRouter()


@router.get(
    "/stocks",
    tags=["Stocks"],
    response_model=list[StockResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all stocks",
    description="Returns all available stocks with optional filtering by exchange and sector.",
)
def get_all_stocks(
    exchange: str | None = Query(
        default=None,
        description="Filter by stock exchange (e.g. NSE)",
    ),
    sector: str | None = Query(
        default=None,
        description="Filter by business sector (e.g. Information Technology)",
    ),
) -> list[StockResponse]:
    """
    Returns all available stocks.

    Optional filters:
    - exchange
    - sector
    """
    return stock_service.get_all_stocks(
        exchange=exchange,
        sector=sector,
    )


@router.get(
    "/stocks/{symbol}",
    tags=["Stocks"],
    response_model=StockResponse,
    status_code=status.HTTP_200_OK,
    summary="Get stock by symbol",
    description="Returns details for a specific stock symbol.",
)
def get_stock_by_symbol(
    symbol: str = Path(
        ...,
        description="Stock symbol (e.g. TCS, INFY, RELIANCE)",
    ),
) -> StockResponse:
    """
    Returns a single stock by its symbol.
    """
    stock = stock_service.get_stock_by_symbol(symbol)

    if stock is None:
        raise StockNotFoundException(symbol)

    return stock