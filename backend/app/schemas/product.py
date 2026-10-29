from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    sku: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=150)

    category_id: int | None = None
    supplier_id: int | None = None

    unit: str = Field(
        default="piece",
        min_length=1,
        max_length=50
    )

    cost_price: Decimal = Field(
        default=0,
        ge=0
    )

    selling_price: Decimal = Field(
        default=0,
        ge=0
    )

    reorder_level: int = Field(
        default=0,
        ge=0
    )
    


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: str | None = None
    name: str | None = None
    category_id: int | None = None
    unit: str | None = None
    supplier_id: int | None = None
    cost_price: Decimal | None = Field(
        default=None,
        ge=0
    )
    selling_price: Decimal | None = Field(
        default=None,
        ge=0
    )
    reorder_level: int | None = Field(
        default=None,
        ge=0
    )


class ProductResponse(ProductBase):
    id: int
    current_stock: int

    model_config = ConfigDict(
        from_attributes=True
    )