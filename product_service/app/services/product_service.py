from typing import List, Optional

from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.brand_repository import BrandRepository

from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from app.schemas.category_schema import CategoryOut
from app.schemas.brand_schema import BrandOut


class ProductService:
    def __init__(
        self,
        product_repo: ProductRepository,
        category_repo: CategoryRepository,
        brand_repo: BrandRepository
    ):
        self.product_repo = product_repo
        self.category_repo = category_repo
        self.brand_repo = brand_repo

    async def create_product(self, product_data: ProductCreate) -> ProductOut:
        # Validasi: category_id harus ada dan valid
        category = await self.category_repo.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {product_data.category_id} not found"
            )

        # Validasi: brand_id harus ada dan valid
        brand = await self.brand_repo.get_by_id(product_data.brand_id)
        if not brand:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Brand with id {product_data.brand_id} not found"
            )

        # Cek apakah SKU sudah dipakai (unique)
        existing = await self.product_repo.get_by_sku(product_data.sku)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SKU '{product_data.sku}' already exists"
            )

        # Semua validasi lolos → create
        return await self.product_repo.create(product_data)

    async def get_all_products(
        self,
        skip: int = 0,
        limit: int = 100,
        populate: bool = False  # nanti bisa dipakai di controller
    ) -> List[ProductOut]:
        products = await self.product_repo.get_all(skip=skip, limit=limit)

        if populate:
            await self._populate_products(products)

        return products

    async def get_product_by_id(
        self,
        product_id: str,
        populate: bool = False
    ) -> ProductOut:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if populate:
            await self._populate_products([product])

        return product

    async def get_product_by_sku(
        self,
        sku: str,
        populate: bool = False
    ) -> ProductOut:
        product = await self.product_repo.get_by_sku(sku)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with SKU '{sku}' not found"
            )

        if populate:
            await self._populate_products([product])

        return product

    async def update_product(
        self,
        product_id: str,
        product_data: ProductUpdate
    ) -> ProductOut:
        # Pastikan product exists
        existing_product = await self.product_repo.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        update_dict = product_data.dict(exclude_unset=True)

        # Validasi category_id jika di-update
        if "category_id" in update_dict:
            category = await self.category_repo.get_by_id(update_dict["category_id"])
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with id {update_dict['category_id']} not found"
                )

        # Validasi brand_id jika di-update
        if "brand_id" in update_dict:
            brand = await self.brand_repo.get_by_id(update_dict["brand_id"])
            if not brand:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Brand with id {update_dict['brand_id']} not found"
                )

        # Validasi SKU unik jika di-update (kecuali sama dengan yang lama)
        if "sku" in update_dict:
            if update_dict["sku"] != existing_product.sku:
                duplicate = await self.product_repo.get_by_sku(update_dict["sku"])
                if duplicate:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"SKU '{update_dict['sku']}' already exists"
                    )

        # Semua validasi lolos → update
        return await self.product_repo.update(product_id, product_data)

    async def delete_product(self, product_id: str) -> None:
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        deleted = await self.product_repo.delete(product_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete product"
            )

    # Helper private: populate category & brand ke dalam list product
    async def _populate_products(self, products: List[ProductOut]) -> None:
        for product in products:
            # Ambil category
            category = await self.category_repo.get_by_id(str(product.category_id))
            if category:
                product.category = CategoryOut(**category.dict())

            # Ambil brand
            brand = await self.brand_repo.get_by_id(str(product.brand_id))
            if brand:
                product.brand = BrandOut(**brand.dict())