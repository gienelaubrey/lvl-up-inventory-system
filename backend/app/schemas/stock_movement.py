from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StockMovementCreate(BaseModel):
    product_id: int

    quantity: int = Field(
        gt=0
    )

    reference: str | None = None
    notes: str | None = None


class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    movement_type: str
    quantity: int
    stock_after: int
    reference: str | None
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )