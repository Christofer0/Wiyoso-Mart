from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Optional, Any
from datetime import datetime

# Attributes bebas (dynamic key-value)
class ProductAttributes(BaseModel):
    color: Optional[str] = None
    storage: Optional[str] = None
    ram: Optional[str] = None
    # Bisa tambah field lain, atau gunakan dict untuk benar-benar dynamic
    # Alternatif: extra: Dict[str, Any] kalau mau fully dynamic
    model_config = {"extra": "allow"}  # izinkan field lain selain yang didefinisikan

class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float
    currency: str = "IDR"
    category_id: str  # ObjectId sebagai string
    brand_id: str     # ObjectId sebagai string
    attributes: ProductAttributes
    images: List[HttpUrl] = []
    status: str = "ACTIVE"  # bisa buat Enum nanti kalau mau lebih ketat

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    attributes: Optional[ProductAttributes] = None
    images: Optional[List[HttpUrl]] = None
    status: Optional[str] = None

class ProductOut(ProductBase):
    id: str = Field(..., alias="_id")
    created_at: datetime
    updated_at: datetime

    # Optional populate relations
    category: Optional["CategoryOut"] = None
    brand: Optional["BrandOut"] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Import setelah definisi untuk forward refs
from .brand_schema import BrandOut
from .category_schema import CategoryOut

ProductOut.update_forward_refs()