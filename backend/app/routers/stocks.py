from fastapi import APIRouter, Path, Query, status

from app.core.exceptions import StockNotFoundException
from app.schemas.stock import (
    StockResponse,
    StockCreate,
    StockUpdate,
)
from app.services.stock_service import stock_service
from app.schemas.stock_history import StockHistoryResponse

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
    page: int = Query(
    default=1,
    ge=1,
    description="Page number",
),

    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of stocks per page",
    ),

    search: str | None = Query(
        default=None,
        description="Search by company name",
    ),

    sort_by: str = Query(
    default="symbol",
    pattern="^(symbol|company_name|current_price|exchange|sector)$",
    description="Field to sort by",
    ),

    order: str = Query(
        default="asc",
        pattern="^(asc|desc)$",
        description="Sort order (asc or desc)",
    ),

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
    page=page,
    limit=limit,
    search=search,
    sort_by=sort_by,
    order=order,
    exchange=exchange,
    sector=sector,
)

@router.get(
    "/stocks/{symbol}/history",
    tags=["Stocks"],
    response_model=list[StockHistoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Get stock price history",
    description="Returns historical price data for a stock.",
)
def get_stock_history(
    symbol: str = Path(
        ...,
        description="Stock symbol (e.g. HDFCBANK, INFY, TCS)",
    ),
    period: str = Query(
        default="1mo",
        pattern="^(1d|5d|1mo|3mo|6mo|1y)$",
        description="Historical data period",
    ),
) -> list[StockHistoryResponse]:
    """
    Returns historical market data for a stock.
    """
    return stock_service.get_stock_history(
        symbol=symbol,
        period=period,
    )

@router.get(
    "/stocks/{symbol}/analysis",
    tags=["Stocks"],
    response_model=StockResponse,
    status_code=status.HTTP_200_OK,
    summary="Get stock market analysis",
    description="Returns stock details along with latest market data.",
)
def get_stock_analysis(
    symbol: str = Path(
        ...,
        description="Stock symbol (e.g. TCS, INFY, RELIANCE)",
    ),
) -> StockResponse:
    """
    Returns stock information with latest market data.
    """
    return stock_service.get_stock_analysis(symbol)
  

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

@router.post(
    "/stocks",
    tags=["Stocks"],
    response_model=StockResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new stock",
    description="Creates a new stock in the database.",
)
def create_stock(
    stock: StockCreate,
) -> StockResponse:
    """
    Creates a new stock.
    """
    return stock_service.create_stock(stock)

@router.put(
    "/stocks/{symbol}",
    tags=["Stocks"],
    response_model=StockResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a stock",
    description="Updates an existing stock by its symbol.",
)
def update_stock(
    symbol: str = Path(
        ...,
        description="Stock symbol (e.g. TCS)",
    ),
    stock: StockUpdate = ...,
) -> StockResponse:
    """
    Updates an existing stock.
    """
    return stock_service.update_stock(
        symbol=symbol,
        stock=stock,
    )
@router.delete(
    "/stocks/{symbol}",
    tags=["Stocks"],
    status_code=status.HTTP_200_OK,
    summary="Delete a stock",
    description="Deletes a stock by its symbol.",
)
def delete_stock(
    symbol: str = Path(
        ...,
        description="Stock symbol (e.g. TCS)",
    ),
) -> dict:
    """
    Deletes a stock by its symbol.
    """
    stock_service.delete_stock(symbol)

    return {
        "success": True,
        "message": f"Stock '{symbol}' deleted successfully.",
        "data": None,
    }