from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut


class CategoryRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["categories"]

    async def create(self, category_data: CategoryCreate) -> CategoryOut:
        doc = category_data.dict()
        now = datetime.utcnow()

        # Convert parent_id ke ObjectId jika valid
        if doc.get("parent_id"):
            if ObjectId.is_valid(doc["parent_id"]):
                doc["parent_id"] = ObjectId(doc["parent_id"])
            else:
                doc["parent_id"] = None

        doc.update({
            "created_at": now,
            "updated_at": now
        })
        result = await self.collection.insert_one(doc)
        return CategoryOut(
            _id=str(result.inserted_id),
            name=doc["name"],
            slug=doc["slug"],
            parent_id=str(doc["parent_id"]) if doc["parent_id"] else None,  # kembali ke str
            created_at=now,
            updated_at=now
        )

    def _doc_to_category(self, doc: dict) -> Optional[CategoryOut]:
        if not doc:
            return None
        return CategoryOut(
            _id=str(doc["_id"]),
            name=doc["name"],
            slug=doc["slug"],
            parent_id=str(doc["parent_id"]) if doc.get("parent_id") else None,
            created_at=doc.get("created_at") or datetime.utcnow(),
            updated_at=doc.get("updated_at") or datetime.utcnow()
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[CategoryOut]:
        categories = []
        cursor = self.collection.find().skip(skip).limit(limit).sort("name", 1)
        async for doc in cursor:
            cat = self._doc_to_category(doc)
            if cat:
                categories.append(cat)
        return categories

    async def get_by_id(self, category_id: str) -> Optional[CategoryOut]:
        if not ObjectId.is_valid(category_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(category_id)})
        return self._doc_to_category(doc)

    async def get_by_slug(self, slug: str) -> Optional[CategoryOut]:
        doc = await self.collection.find_one({"slug": slug})
        return self._doc_to_category(doc)

    async def update(self, category_id: str, category_data: CategoryUpdate) -> Optional[CategoryOut]:
        if not ObjectId.is_valid(category_id):
            return None

        update_data = category_data.dict(exclude_unset=True)

        if "parent_id" in update_data:
            if update_data["parent_id"] is not None and ObjectId.is_valid(update_data["parent_id"]):
                update_data["parent_id"] = ObjectId(update_data["parent_id"])
            else:
                update_data["parent_id"] = None

        if not update_data:
            return await self.get_by_id(category_id)

        update_data["updated_at"] = datetime.utcnow()

        await self.collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": update_data}
        )
        return await self.get_by_id(category_id)

    async def delete(self, category_id: str) -> bool:
        if not ObjectId.is_valid(category_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(category_id)})
        return result.deleted_count > 0

    async def get_children(self, parent_id: str) -> List[CategoryOut]:
        if not ObjectId.is_valid(parent_id):
            return []
        children = []
        cursor = self.collection.find({"parent_id": ObjectId(parent_id)})
        async for doc in cursor:
            child = self._doc_to_category(doc)
            if child:
                children.append(child)
        return children