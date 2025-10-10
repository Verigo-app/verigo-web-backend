# app/schemas/product.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


# ---------- Base Schemas ----------
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    pic_url: Optional[str] = None
    barcode_url: Optional[str] = None
    barcode_value: Optional[str] = None
    verified: Optional[bool] = False


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    business_id: int
    category_name: Optional[str] = None  # user can pass category name


class ProductUpdate(ProductBase):
    """Schema for updating an existing product"""
    pass


# ---------- Nested Category ----------
class CategoryOut(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Product Output ----------
class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    pic_url: str
    category: Optional[CategoryOut]   # nested object

    average_rating: Optional[float] = 0.0
    total_views: Optional[int] = 0
    total_scans: Optional[int] = 0
    is_verified: Optional[bool] = False
    promotion_title: Optional[str] = None
    promotion_discount: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
