from pydantic import BaseModel, Field


class StockResponse(BaseModel):
    symbol: str = Field(..., description="Stock symbol")

    company_name: str = Field(
        ...,
        description="Full company name",
    )

    exchange: str = Field(
        ...,
        description="Stock exchange",
    )

    current_price: float = Field(
        ...,
        description="Current market price",
    )

    currency: str = Field(
        ...,
        description="Trading currency",
    )

    sector: str = Field(
        ...,
        description="Business sector",
    )

    previous_close: float | None = Field(
    default=None,
    description="Previous closing price",
    )

    day_high: float | None = Field(
        default=None,
        description="Highest price during the trading day",
    )

    day_low: float | None = Field(
        default=None,
        description="Lowest price during the trading day",
    )

    volume: int | None = Field(
        default=None,
        description="Trading volume",
    )

    

class StockCreate(BaseModel):
    symbol: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Unique stock symbol",
        example="TCS",
    )

    company_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Company name",
        example="Tata Consultancy Services",
    )

    exchange: str = Field(
        ...,
        min_length=2,
        max_length=10,
        description="Stock exchange",
        example="NSE",
    )

    current_price: float = Field(
        ...,
        gt=0,
        description="Current stock price",
        example=3875.30,
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Currency",
        example="INR",
    )

    sector: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Business sector",
        example="Information Technology",
    )         

    model_config = {
        "json_schema_extra": {
            "example": {
                "symbol": "TCS",
                "company_name": "Tata Consultancy Services",
                "exchange": "NSE",
                "current_price": 3875.30,
                "currency": "INR",
                "sector": "Information Technology",
            }
        }
    }

class StockUpdate(BaseModel):
    company_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Company name",
        example="Tata Consultancy Services",
    )

    exchange: str = Field(
        ...,
        min_length=2,
        max_length=10,
        description="Stock exchange",
        example="NSE",
    )

    current_price: float = Field(
        ...,
        gt=0,
        description="Updated stock price",
        example=3925.80,
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="Currency",
        example="INR",
    )

    sector: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Business sector",
        example="Information Technology",
    )    

