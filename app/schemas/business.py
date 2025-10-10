# app/schemas/business.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BusinessCreate(BaseModel):
    brand_name: str
    category: Optional[str] = None
    picture_url: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None

class BusinessUpdate(BaseModel):
    brand_name: Optional[str] = None
    category: Optional[str] = None
    picture_url: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None

class BusinessOut(BaseModel):
    id: int
    user_id: int
    brand_name: str
    category: Optional[str]
    picture_url: Optional[str]
    address: Optional[str]
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
