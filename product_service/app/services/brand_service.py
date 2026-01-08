from typing import List, Optional

from fastapi import HTTPException, status

from app.repositories.brand_repository import BrandRepository
from app.schemas.brand_schema import BrandCreate, BrandUpdate, BrandOut


class BrandService:
    def __init__(self, brand_repo: BrandRepository):
        self.brand_repo = brand_repo

    async def create_brand(self, brand_data: BrandCreate) -> BrandOut:
        # Validasi: slug harus unik
        existing_slug = await self.brand_repo.get_by_slug(brand_data.slug)
        if existing_slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slug '{brand_data.slug}' already exists"
            )

        # Optional: validasi name unik (jika diinginkan)
        # existing_name = await self.brand_repo.collection.find_one({"name": brand_data.name})
        # if existing_name:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=f"Brand name '{brand_data.name}' already exists"
        #     )

        return await self.brand_repo.create(brand_data)

    async def get_all_brands(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[BrandOut]:
        return await self.brand_repo.get_all(skip=skip, limit=limit)

    async def get_brand_by_id(self, brand_id: str) -> BrandOut:
        brand = await self.brand_repo.get_by_id(brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )
        return brand

    async def get_brand_by_slug(self, slug: str) -> BrandOut:
        brand = await self.brand_repo.get_by_slug(slug)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Brand with slug '{slug}' not found"
            )
        return brand

    async def update_brand(
        self,
        brand_id: str,
        brand_data: BrandUpdate
    ) -> BrandOut:
        # Pastikan brand exists
        existing_brand = await self.brand_repo.get_by_id(brand_id)
        if not existing_brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )

        update_dict = brand_data.dict(exclude_unset=True)

        # Validasi slug unik jika di-update
        if "slug" in update_dict:
            if update_dict["slug"] != existing_brand.slug:
                duplicate = await self.brand_repo.get_by_slug(update_dict["slug"])
                if duplicate:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Slug '{update_dict['slug']}' already exists"
                    )

        # Optional: validasi name unik jika di-update
        # if "name" in update_dict and update_dict["name"] != existing_brand.name:
        #     duplicate_name = await self.brand_repo.collection.find_one({"name": update_dict["name"]})
        #     if duplicate_name:
        #         raise HTTPException(
        #             status_code=status.HTTP_400_BAD_REQUEST,
        #             detail=f"Brand name '{update_dict['name']}' already exists"
        #         )

        return await self.brand_repo.update(brand_id, brand_data)

    async def delete_brand(self, brand_id: str) -> None:
        # Pastikan brand exists
        brand = await self.brand_repo.get_by_id(brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Brand not found"
            )

        # Optional: cek apakah brand sedang dipakai di product
        # product_count = await self.brand_repo.db["products"].count_documents({"brand_id": ObjectId(brand_id)})
        # if product_count > 0:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Cannot delete brand because it is used by one or more products"
        #     )

        deleted = await self.brand_repo.delete(brand_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete brand"
            )