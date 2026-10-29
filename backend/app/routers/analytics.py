from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.models.stock_movement import StockMovement
from app.models.supplier import Supplier
from app.schemas.analytics import SupplierSalesAnalytics


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get(
    "/sales-by-supplier",
    response_model=list[SupplierSalesAnalytics]
)
def sales_by_supplier(
    db: Session = Depends(get_db)
):
    units_sold = func.coalesce(
        func.sum(StockMovement.quantity),
        0
    )

    sales_value = func.coalesce(
        func.sum(
            StockMovement.quantity
            * Product.selling_price
        ),
        0
    )

    rows = (
        db.query(
            Supplier.id.label("supplier_id"),
            Supplier.name.label("supplier_name"),
            Product.sku,
            Product.name.label("product_name"),
            units_sold.label("units_sold"),
            sales_value.label("sales_value"),
        )
        .join(
            Product,
            Product.supplier_id == Supplier.id
        )
        .outerjoin(
            StockMovement,
            and_(
                StockMovement.product_id
                == Product.id,

                StockMovement.movement_type
                == "OUT",

                StockMovement.reason
                == "SALE",
            )
        )
        .group_by(
            Supplier.id,
            Supplier.name,
            Product.id,
            Product.sku,
            Product.name,
            Product.selling_price,
        )
        .order_by(
            Supplier.name.asc(),
            units_sold.desc(),
        )
        .all()
    )

    grouped = defaultdict(list)

    supplier_names = {}

    for row in rows:
        supplier_names[
            row.supplier_id
        ] = row.supplier_name

        grouped[
            row.supplier_id
        ].append(
            {
                "sku": row.sku,
                "product_name": row.product_name,
                "units_sold": int(
                    row.units_sold
                ),
                "sales_value":
                    row.sales_value,
            }
        )

    return [
        {
            "supplier_id": supplier_id,
            "supplier_name":
                supplier_names[supplier_id],
            "products":
                grouped[supplier_id],
        }
        for supplier_id in grouped
    ]