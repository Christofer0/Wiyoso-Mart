from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional

from config.mongo_config import db
from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.brand_repository import BrandRepository
from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut

router = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Dependency: buat ProductService dengan semua repo yang dibutuhkan
def get_product_service() -> ProductService:
    product_repo = ProductRepository(db)
    category_repo = CategoryRepository(db)
    brand_repo = BrandRepository(db)
    return ProductService(
        product_repo=product_repo,
        category_repo=category_repo,
        brand_repo=brand_repo
    )

@router.post(
    "/",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product"
)
async def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    return await service.create_product(product_data)

@router.get(
    "/",
    response_model=List[ProductOut],
    summary="Get all products with optional filters"
)
async def get_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    brand_id: Optional[str] = Query(None, description="Filter by brand ID"),
    populate: bool = Query(False, description="Include full category and brand details"),
    service: ProductService = Depends(get_product_service)
):
    """
    Ambil semua produk dengan filter opsional.
    - populate=true → tampilkan object category & brand lengkap
    """
    # Jika ada filter category atau brand, kita bisa tambah logic di service nanti
    # Untuk sekarang, kita ambil semua dulu (bisa diperluas)
    products = await service.get_all_products(skip=skip, limit=limit, populate=populate)

    # Optional future: filter manual jika diperlukan
    # if category_id or brand_id:
    #     products = [p for p in products if 
    #         (not category_id or str(p.category_id) == category_id) and
    #         (not brand_id or str(p.brand_id) == brand_id)]

    return products

@router.get(
    "/sku/{sku}",
    response_model=ProductOut,
    summary="Get product by SKU"
)
async def get_product_by_sku(
    sku: str,
    populate: bool = Query(False),
    service: ProductService = Depends(get_product_service)
):
    return await service.get_product_by_sku(sku, populate=populate)

@router.get(
    "/{product_id}",
    response_model=ProductOut,
    summary="Get product by ID"
)
async def get_product_by_id(
    product_id: str,
    populate: bool = Query(False),
    service: ProductService = Depends(get_product_service)
):
    return await service.get_product_by_id(product_id, populate=populate)

@router.put(
    "/{product_id}",
    response_model=ProductOut,
    summary="Update a product"
)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    return await service.update_product(product_id, product_data)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product"
)
async def delete_product(
    product_id: str,
    service: ProductService = Depends(get_product_service)
):
    await service.delete_product(product_id)
    return None