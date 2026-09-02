from datetime import datetime

from pydantic import BaseModel, Field


class PaperTradeRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    quantity: float = Field(gt=0)


class PaperAccountResponse(BaseModel):
    user_id: str
    starting_balance: float
    cash_balance: float
    invested_value: float
    current_value: float
    total_profit_loss: float
    total_return_percentage: float


class PaperPositionResponse(BaseModel):
    symbol: str
    quantity: float
    average_price: float
    current_price: float
    invested_value: float
    current_value: float
    profit_loss: float
    profit_loss_percentage: float


class PaperTradeResponse(BaseModel):
    id: str
    symbol: str
    side: str
    quantity: float
    price: float
    total_value: float
    realized_profit_loss: float = 0
    created_at: datetime


class PaperAllocationResponse(BaseModel):

    symbol: str
    value: float
    percentage: float


class PaperPortfolioResponse(BaseModel):
    cash_balance: float
    invested_value: float
    current_value: float
    total_profit_loss: float
    total_return_percentage: float
    positions: list[PaperPositionResponse]
    allocation: list[PaperAllocationResponse]