from fastapi import APIRouter

from app.services.stock_service import stock_service

router = APIRouter()


@router.get("/stocks", tags=["Stocks"])
def get_all_stocks() -> list[dict]:
    """Returns all available stocks."""
    return stock_service.get_all_stocks()