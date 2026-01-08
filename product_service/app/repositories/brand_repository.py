from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from app.schemas.brand_schema import BrandCreate, BrandUpdate, BrandOut


class BrandRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["brands"]

    async def create(self, brand_data: BrandCreate) -> BrandOut:
        doc = brand_data.dict()
        now = datetime.utcnow()
        doc.update({
            "created_at": now,
            "updated_at": now
        })
        result = await self.collection.insert_one(doc)
        return BrandOut(
            _id=str(result.inserted_id),  # pakai _id karena alias di schema
            name=doc["name"],
            slug=doc["slug"],
            created_at=now,
            updated_at=now
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[BrandOut]:
        brands = []
        cursor = self.collection.find().skip(skip).limit(limit).sort("name", 1)
        async for doc in cursor:
            brand = self._doc_to_brand(doc)
            if brand:
                brands.append(brand)
        return brands

    async def get_by_id(self, brand_id: str) -> Optional[BrandOut]:
        if not ObjectId.is_valid(brand_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(brand_id)})
        return self._doc_to_brand(doc)

    async def get_by_slug(self, slug: str) -> Optional[BrandOut]:
        doc = await self.collection.find_one({"slug": slug})
        return self._doc_to_brand(doc)

    async def update(self, brand_id: str, brand_data: BrandUpdate) -> Optional[BrandOut]:
        if not ObjectId.is_valid(brand_id):
            return None

        update_data = {k: v for k, v in brand_data.dict(exclude_unset=True).items()}
        if not update_data:
            return await self.get_by_id(brand_id)

        update_data["updated_at"] = datetime.utcnow()

        await self.collection.update_one(
            {"_id": ObjectId(brand_id)},
            {"$set": update_data}
        )
        return await self.get_by_id(brand_id)

    async def delete(self, brand_id: str) -> bool:
        if not ObjectId.is_valid(brand_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(brand_id)})
        return result.deleted_count > 0

    def _doc_to_brand(self, doc: dict) -> Optional[BrandOut]:
        if not doc:
            return None
        # Pastikan created_at dan updated_at ada, kalau tidak kasih default now()
        created_at = doc.get("created_at") or datetime.utcnow()
        updated_at = doc.get("updated_at") or datetime.utcnow()

        return BrandOut(
            _id=str(doc["_id"]),  # penting: pakai _id karena alias di schema
            name=doc["name"],
            slug=doc["slug"],
            created_at=created_at,
            updated_at=updated_at
        )