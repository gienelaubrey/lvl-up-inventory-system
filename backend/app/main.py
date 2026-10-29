from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.category import Category
from app.models.product import Product
from app.models.stock_movement import StockMovement


from app.routers.categories import router as categories_router
from app.routers.products import router as products_router
from app.routers.inventory import router as inventory_router
from app.routers.suppliers import router as suppliers_router
from app.routers.analytics import router as analytics_router



app = FastAPI(
    title="LVL UP Inventory API",
    description="Inventory Management API for LVL UP Enterprises OPC",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(inventory_router)
app.include_router(suppliers_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "message": "LVL UP Inventory API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }