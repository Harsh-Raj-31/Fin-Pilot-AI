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