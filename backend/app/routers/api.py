from fastapi import APIRouter

from app.routers.health import router as health_router
from app.routers.home import router as home_router
from app.routers.stocks import router as stocks_router
from app.routers.portfolio import router as portfolio_router

api_router = APIRouter()

api_router.include_router(home_router)
api_router.include_router(health_router)
api_router.include_router(stocks_router)
api_router.include_router(portfolio_router)