from typing import List, Optional

from fastapi import HTTPException, status
from bson import ObjectId

from app.repositories.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def create_category(self, category_data: CategoryCreate) -> CategoryOut:
        # Validasi slug unik
        existing_slug = await self.category_repo.get_by_slug(category_data.slug)
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slug '{category_data.slug}' already exists"
            )

        # Validasi parent_id jika diisi
        if category_data.parent_id:
            parent = await self.category_repo.get_by_id(category_data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Parent category with id {category_data.parent_id} not found"
                )

        return await self.category_repo.create(category_data)

    async def get_all_categories(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[CategoryOut]:
        return await self.category_repo.get_all(skip=skip, limit=limit)

    async def get_category_by_id(self, category_id: str) -> CategoryOut:
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return category

    async def get_category_by_slug(self, slug: str) -> CategoryOut:
        category = await self.category_repo.get_by_slug(slug)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with slug '{slug}' not found"
            )
        return category

    async def get_children_categories(self, parent_id: str) -> List[CategoryOut]:
        parent = await self.category_repo.get_by_id(parent_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parent category with id {parent_id} not found"
            )
        return await self.category_repo.get_children(parent_id)

    async def update_category(
        self,
        category_id: str,
        category_data: CategoryUpdate
    ) -> CategoryOut:
        # Pastikan category exists
        existing_category = await self.category_repo.get_by_id(category_id)
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        update_dict = category_data.dict(exclude_unset=True)

        # Validasi slug unik jika di-update
        if "slug" in update_dict:
            if update_dict["slug"] != existing_category.slug:
                duplicate = await self.category_repo.get_by_slug(update_dict["slug"])
                if duplicate:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Slug '{update_dict['slug']}' already exists"
                    )

        # Validasi parent_id jika di-update
        if "parent_id" in update_dict:
            new_parent_id = update_dict["parent_id"]

            # Tidak boleh jadi parent dirinya sendiri
            if new_parent_id and new_parent_id == category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A category cannot be its own parent"
                )

            # Jika parent_id diisi, pastikan parent exists
            if new_parent_id:
                parent = await self.category_repo.get_by_id(new_parent_id)
                if not parent:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Parent category with id {new_parent_id} not found"
                    )

        return await self.category_repo.update(category_id, category_data)

    async def delete_category(self, category_id: str) -> None:
        # Pastikan category exists
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        # Optional: cek apakah ada children
        children = await self.category_repo.get_children(category_id)
        if children:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete category because it has child categories"
            )

        # Optional: cek apakah category dipakai di product
        # product_count = await self.category_repo.collection.db["products"].count_documents(
        #     {"category_id": ObjectId(category_id)}
        # )
        # if product_count > 0:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Cannot delete category because it is used by one or more products"
        #     )

        deleted = await self.category_repo.delete(category_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete category"
            )