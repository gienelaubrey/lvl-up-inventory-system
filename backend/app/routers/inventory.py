from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import (
    StockMovementCreate,
    StockMovementResponse,
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post(
    "/stock-in",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED
)
def stock_in(
    data: StockMovementCreate,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == data.product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    product.current_stock += data.quantity
    reason = (data.reason or "RECEIPT").upper()

    movement = StockMovement(
        product_id=product.id,
        movement_type="IN",
        reason=reason,
        quantity=data.quantity,
        stock_after=product.current_stock,
        reference=data.reference,
        notes=data.notes,
    )

    db.add(movement)
    db.commit()

    db.refresh(product)
    db.refresh(movement)

    return movement


@router.post(
    "/stock-out",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED
)
def stock_out(
    data: StockMovementCreate,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == data.product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.current_stock < data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )

    product.current_stock -= data.quantity
    reason = (data.reason or "SALE").upper()

    movement = StockMovement(
        product_id=product.id,
        movement_type="OUT",
        reason=reason,
        quantity=data.quantity,
        stock_after=product.current_stock,
        reference=data.reference,
        notes=data.notes,
    )

    db.add(movement)
    db.commit()

    db.refresh(product)
    db.refresh(movement)

    return movement


@router.get(
    "/movements",
    response_model=list[StockMovementResponse]
)
def get_stock_movements(
    db: Session = Depends(get_db)
):
    return (
        db.query(StockMovement)
        .order_by(
            StockMovement.created_at.desc()
        )
        .all()
    )