from fastapi import FastAPI
from config.mongo_config import client

from app.controllers.brand_controller import router as brand_router
from app.controllers.category_controller import router as category_router
from app.controllers.product_controller import router as product_router

app = FastAPI(
    title="E-Commerce API",
    description="FastAPI + MongoDB - Clean Layered Architecture",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db():
    try:
        await client.admin.command("ping")
        print("✅ MongoDB connection successful")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

@app.on_event("shutdown")
async def shutdown_db():
    client.close()

@app.get("/")
async def root():
    return {"message": "Welcome to E-Commerce API! Visit /docs for Swagger UI"}

# Include all routers
app.include_router(brand_router)
app.include_router(category_router)
app.include_router(product_router)