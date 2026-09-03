from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.core.dependencies import get_current_user
from app.schemas.watchlist import (
    WatchlistActionResponse,
    WatchlistCreate,
    WatchlistItemResponse,
)
from app.services.watchlist_service import watchlist_service


router = APIRouter(
    prefix="/watchlist",
    tags=["Watchlist"],
)


@router.get(
    "",
    response_model=list[WatchlistItemResponse],
    status_code=status.HTTP_200_OK,
    summary="Get user watchlist",
    description=(
        "Returns the authenticated user's watchlist "
        "with current market information."
    ),
)
def get_watchlist(
    current_user: dict = Depends(
        get_current_user
    ),
) -> list[WatchlistItemResponse]:

    user_id = current_user["id"]

    return watchlist_service.get_watchlist(
        user_id
    )


@router.post(
    "",
    response_model=WatchlistActionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add stock to watchlist",
    description=(
        "Adds a stock to the authenticated user's watchlist."
    ),
)
def add_to_watchlist(
    watchlist: WatchlistCreate,
    current_user: dict = Depends(
        get_current_user
    ),
) -> WatchlistActionResponse:

    user_id = current_user["id"]

    try:
        watchlist_service.add_stock(
            user_id,
            watchlist.symbol,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e

    return WatchlistActionResponse(
        success=True,
        message=(
            f"{watchlist.symbol.upper()} "
            "added to your watchlist."
        ),
    )


@router.delete(
    "/{symbol}",
    response_model=WatchlistActionResponse,
    status_code=status.HTTP_200_OK,
    summary="Remove stock from watchlist",
    description=(
        "Removes a stock from the authenticated user's watchlist."
    ),
)
def remove_from_watchlist(
    symbol: str = Path(
        ...,
        min_length=1,
        max_length=20,
        description="Stock symbol to remove",
        example="TCS",
    ),
    current_user: dict = Depends(
        get_current_user
    ),
) -> WatchlistActionResponse:

    user_id = current_user["id"]

    watchlist_service.remove_stock(
        user_id,
        symbol,
    )

    return WatchlistActionResponse(
        success=True,
        message=(
            f"{symbol.upper()} "
            "removed from your watchlist."
        ),
    )