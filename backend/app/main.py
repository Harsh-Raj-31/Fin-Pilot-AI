# Standard Library
from contextlib import asynccontextmanager

# Third-Party Libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local Application Imports
from app.config import settings
from app.core.handlers import register_exception_handlers
from app.routers.api import api_router
from app.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 FinPilot AI starting...")
    yield
    logger.info("🛑 FinPilot AI shutting down...")


app = FastAPI(
    title="FinPilot AI API",
    description="Multi-Agent Investment Intelligence Platform",
    version=settings.API_VERSION,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(
    api_router,
    prefix="/api/v1",
)

# steps to run backend
# cd C:\Projects\Fin-Pilot-AI\backend
# .venv\Scripts\activate
# python -m uvicorn app.main:app --reload