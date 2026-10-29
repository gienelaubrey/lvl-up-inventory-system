from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    sku = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=True
    )
    
    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=True
    )

    unit = Column(
        String(50),
        nullable=False,
        default="piece"
    )

    cost_price = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    selling_price = Column(
        Numeric(12, 2),
        nullable=False,
        default=0
    )

    current_stock = Column(
        Integer,
        nullable=False,
        default=0
    )

    reorder_level = Column(
        Integer,
        nullable=False,
        default=0
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    supplier = relationship(
        "Supplier",
        back_populates="products"
    )