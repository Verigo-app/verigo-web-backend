# app/schemas/promotion.py
from pydantic import BaseModel
from datetime import datetime

class PromotionBase(BaseModel):
    product_id: int
    title: str
    description: str | None = None
    discount_percent: float
    start_date: datetime
    end_date: datetime

class PromotionCreate(PromotionBase):
    pass

class PromotionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    discount_percent: float | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    is_active: bool | None = None

class PromotionOut(PromotionBase):
    id: int
    business_id: int
    is_active: bool

    class Config:
        orm_mode = True
