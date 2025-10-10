# app/models/promotion.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float, Numeric
from datetime import datetime
from app.models.base import Base

class Promotion(Base):
    __tablename__ = "promotions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    business_id = Column(Integer, ForeignKey("businesses.id"))
    title = Column(String)
    description = Column(Text)
    discount_percent = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
