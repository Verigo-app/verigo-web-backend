# app/models/analytics.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Numeric
from datetime import datetime
from app.models.base import Base

class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id")) #customer who scanned the product
    feedback = Column(Text)
    rating = Column(Integer)
    views = Column(Integer, default=0) 
    scans = Column(Integer, default=0)  
    created_at = Column(DateTime, default=datetime.utcnow)