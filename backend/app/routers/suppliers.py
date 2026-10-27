from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.supplier import Supplier
from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse,
    SupplierUpdate,
)


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)


@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db)
):
    existing_supplier = (
        db.query(Supplier)
        .filter(Supplier.name == supplier.name)
        .first()
    )

    if existing_supplier:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Supplier already exists"
        )

    new_supplier = Supplier(
        name=supplier.name,
        contact_person=supplier.contact_person,
        phone=supplier.phone,
        email=supplier.email,
        address=supplier.address,
        notes=supplier.notes,
    )

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return new_supplier


@router.get(
    "",
    response_model=list[SupplierResponse]
)
def get_suppliers(
    db: Session = Depends(get_db)
):
    return (
        db.query(Supplier)
        .order_by(Supplier.name.asc())
        .all()
    )


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    return supplier


@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    db: Session = Depends(get_db)
):
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    update_data = supplier_data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        duplicate = (
            db.query(Supplier)
            .filter(
                Supplier.name == update_data["name"],
                Supplier.id != supplier_id,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Supplier already exists"
            )

    for field, value in update_data.items():
        setattr(supplier, field, value)

    db.commit()
    db.refresh(supplier)

    return supplier


@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )

    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )

    db.delete(supplier)
    db.commit()

    return None