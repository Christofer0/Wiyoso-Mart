from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    slug: str
    parent_id: Optional[str] = None  # string karena nanti dari ObjectId

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[str] = None  # bisa di-set ke None untuk hapus parent

class CategoryOut(CategoryBase):
    id: str = Field(..., alias="_id")
    created_at: datetime
    updated_at: datetime

    # Optional: kalau nanti mau populate parent category
    parent: Optional["CategoryOut"] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Untuk menghindari circular import error saat define parent
CategoryOut.update_forward_refs()