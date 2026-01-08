from fastapi import APIRouter, Depends, status
from typing import List

from config.mongo_config import db
from app.repositories.category_repository import CategoryRepository
from app.services.category_service import CategoryService
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter(
    prefix="/api/categories",
    tags=["categories"],
    responses={404: {"description": "Not found"}},
)

# Dependency injection untuk CategoryService
def get_category_service() -> CategoryService:
    repo = CategoryRepository(db)
    return CategoryService(category_repo=repo)

@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category"
)
async def create_category(
    category_data: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    """
    Create a new category.
    - parent_id bersifat opsional (None untuk root category)
    """
    return await service.create_category(category_data)

@router.get(
    "/",
    response_model=List[CategoryOut],
    summary="Get all categories"
)
async def get_all_categories(
    skip: int = 0,
    limit: int = 100,
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_all_categories(skip=skip, limit=limit)

@router.get(
    "/{category_id}",
    response_model=CategoryOut,
    summary="Get category by ID"
)
async def get_category_by_id(
    category_id: str,
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_category_by_id(category_id)

@router.get(
    "/slug/{slug}",
    response_model=CategoryOut,
    summary="Get category by slug"
)
async def get_category_by_slug(
    slug: str,
    service: CategoryService = Depends(get_category_service)
):
    return await service.get_category_by_slug(slug)

@router.get(
    "/{category_id}/children",
    response_model=List[CategoryOut],
    summary="Get child categories of a parent category"
)
async def get_children_categories(
    category_id: str,
    service: CategoryService = Depends(get_category_service)
):
    """
    Mengembalikan semua subcategory langsung (level 1) dari category_id yang diberikan.
    """
    return await service.get_children_categories(category_id)

@router.put(
    "/{category_id}",
    response_model=CategoryOut,
    summary="Update a category"
)
async def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    service: CategoryService = Depends(get_category_service)
):
    return await service.update_category(category_id, category_data)

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category"
)
async def delete_category(
    category_id: str,
    service: CategoryService = Depends(get_category_service)
):
    await service.delete_category(category_id)
    return None