from decimal import Decimal

from pydantic import BaseModel


class ProductSalesRank(BaseModel):
    sku: str
    product_name: str
    units_sold: int
    sales_value: Decimal


class SupplierSalesAnalytics(BaseModel):
    supplier_id: int
    supplier_name: str
    products: list[ProductSalesRank]