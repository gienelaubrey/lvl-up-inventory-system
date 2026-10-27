from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierBase(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150
    )

    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    notes: str | None = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: str | None = None
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    notes: str | None = None


class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )