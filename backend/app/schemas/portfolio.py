from pydantic import BaseModel, Field


class PortfolioCreate(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    quantity: float = Field(gt=0)
    average_price: float = Field(gt=0)

class PortfolioResponse(BaseModel):
    id: str
    symbol: str
    quantity: float
    average_price: float

class PortfolioUpdate(BaseModel):
    quantity: float = Field(gt=0)
    average_price: float = Field(gt=0)