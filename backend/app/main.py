from app.config import settings
from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.api import api_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 FinPilot AI starting...")
    yield
    print("🛑 FinPilot AI shutting down...")


app = FastAPI(
    title="FinPilot AI API",
    description="Multi-Agent Investment Intelligence Platform",
    version=settings.API_VERSION,
    lifespan=lifespan,
)

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