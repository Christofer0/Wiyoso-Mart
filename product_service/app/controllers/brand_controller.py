from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from config.mongo_config import db  # db = client[DB_NAME]
from app.repositories.brand_repository import BrandRepository
from app.services.brand_service import BrandService
from app.schemas.brand_schema import BrandCreate, BrandUpdate, BrandOut

router = APIRouter(
    prefix="/api/brands",
    tags=["brands"],
    responses={404: {"description": "Not found"}},
)

# Dependency: buat BrandService dengan repo yang inject db
def get_brand_service() -> BrandService:
    repo = BrandRepository(db)
    return BrandService(brand_repo=repo)

@router.post(
    "/",
    response_model=BrandOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new brand"
)
async def create_brand(
    brand_data: BrandCreate,
    service: BrandService = Depends(get_brand_service)
):
    return await service.create_brand(brand_data)

@router.get(
    "/",
    response_model=List[BrandOut],
    summary="Get all brands"
)
async def get_all_brands(
    skip: int = 0,
    limit: int = 100,
    service: BrandService = Depends(get_brand_service)
):
    return await service.get_all_brands(skip=skip, limit=limit)

@router.get(
    "/{brand_id}",
    response_model=BrandOut,
    summary="Get brand by ID"
)
async def get_brand_by_id(
    brand_id: str,
    service: BrandService = Depends(get_brand_service)
):
    return await service.get_brand_by_id(brand_id)

@router.get(
    "/slug/{slug}",
    response_model=BrandOut,
    summary="Get brand by slug"
)
async def get_brand_by_slug(
    slug: str,
    service: BrandService = Depends(get_brand_service)
):
    return await service.get_brand_by_slug(slug)

@router.put(
    "/{brand_id}",
    response_model=BrandOut,
    summary="Update a brand"
)
async def update_brand(
    brand_id: str,
    brand_data: BrandUpdate,
    service: BrandService = Depends(get_brand_service)
):
    return await service.update_brand(brand_id, brand_data)

@router.delete(
    "/{brand_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a brand"
)
async def delete_brand(
    brand_id: str,
    service: BrandService = Depends(get_brand_service)
):
    await service.delete_brand(brand_id)
    return None  # 204 No Content