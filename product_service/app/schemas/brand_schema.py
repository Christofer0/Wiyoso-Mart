from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BrandBase(BaseModel):
    name: str
    slug: str

class BrandCreate(BrandBase):
    pass  # sama dengan base, tidak ada field tambahan

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None

class BrandOut(BrandBase):
    id: str = Field(..., alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }