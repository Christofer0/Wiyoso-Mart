from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut


class ProductRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["products"]

    async def create(self, product_data: ProductCreate) -> ProductOut:
        # Ambil dict, tapi images masih HttpUrl object
        data_dict = product_data.dict()

        # Convert images jadi list string
        images_str = [str(url) for url in data_dict["images"]]

        now = datetime.utcnow()

        doc = {
            "sku": data_dict["sku"],
            "name": data_dict["name"],
            "description": data_dict.get("description"),
            "price": data_dict["price"],
            "currency": data_dict["currency"],
            "category_id": ObjectId(data_dict["category_id"]),
            "brand_id": ObjectId(data_dict["brand_id"]),
            "attributes": data_dict["attributes"],
            "images": images_str,  # ← ini yang penting: list[str]
            "status": data_dict.get("status", "ACTIVE"),
            "created_at": now,
            "updated_at": now
        }

        result = await self.collection.insert_one(doc)

        return ProductOut(
            _id=str(result.inserted_id),
            sku=doc["sku"],
            name=doc["name"],
            description=doc["description"],
            price=doc["price"],
            currency=doc["currency"],
            category_id=str(doc["category_id"]),
            brand_id=str(doc["brand_id"]),
            attributes=doc["attributes"],
            images=doc["images"],  # sudah list str, aman untuk Pydantic
            status=doc["status"],
            created_at=now,
            updated_at=now
        )

    def _doc_to_product(self, doc: dict) -> Optional[ProductOut]:
        if not doc:
            return None

        return ProductOut(
            _id=str(doc["_id"]),
            sku=doc["sku"],
            name=doc["name"],
            description=doc.get("description"),
            price=doc["price"],
            currency=doc["currency"],
            category_id=str(doc["category_id"]),
            brand_id=str(doc["brand_id"]),
            attributes=doc.get("attributes", {}),
            images=doc.get("images", []),
            status=doc.get("status", "ACTIVE"),
            created_at=doc.get("created_at") or datetime.utcnow(),
            updated_at=doc.get("updated_at") or datetime.utcnow()
        )

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductOut]:
        products = []
        cursor = self.collection.find().skip(skip).limit(limit).sort("created_at", -1)
        async for doc in cursor:
            product = self._doc_to_product(doc)
            if product:
                products.append(product)
        return products

    async def get_by_id(self, product_id: str) -> Optional[ProductOut]:
        if not ObjectId.is_valid(product_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(product_id)})
        return self._doc_to_product(doc)

    async def get_by_sku(self, sku: str) -> Optional[ProductOut]:
        doc = await self.collection.find_one({"sku": sku})
        return self._doc_to_product(doc)

    async def update(self, product_id: str, product_data: ProductUpdate) -> Optional[ProductOut]:
        if not ObjectId.is_valid(product_id):
            return None

        update_dict = product_data.dict(exclude_unset=True)

        # Convert images jika ada
        if "images" in update_dict:
            update_dict["images"] = [str(url) for url in update_dict["images"]]

        # Convert ID jika ada
        if "category_id" in update_dict and update_dict["category_id"] is not None:
            update_dict["category_id"] = ObjectId(update_dict["category_id"])
        if "brand_id" in update_dict and update_dict["brand_id"] is not None:
            update_dict["brand_id"] = ObjectId(update_dict["brand_id"])

        if not update_dict:
            return await self.get_by_id(product_id)

        update_dict["updated_at"] = datetime.utcnow()

        await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_dict}
        )

        return await self.get_by_id(product_id)

    async def delete(self, product_id: str) -> bool:
        if not ObjectId.is_valid(product_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0

    # Optional: helper untuk filter
    async def get_by_category(self, category_id: str, skip: int = 0, limit: int = 100) -> List[ProductOut]:
        if not ObjectId.is_valid(category_id):
            return []
        products = []
        cursor = self.collection.find({"category_id": ObjectId(category_id)}).skip(skip).limit(limit)
        async for doc in cursor:
            products.append(self._doc_to_product(doc))
        return products

    async def get_by_brand(self, brand_id: str, skip: int = 0, limit: int = 100) -> List[ProductOut]:
        if not ObjectId.is_valid(brand_id):
            return []
        products = []
        cursor = self.collection.find({"brand_id": ObjectId(brand_id)}).skip(skip).limit(limit)
        async for doc in cursor:
            products.append(self._doc_to_product(doc))
        return products