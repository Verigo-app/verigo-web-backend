# app/models/product.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True) 
    category_name = Column(String, nullable=True)
    name = Column(String)
    description = Column(Text)
    pic_url = Column(String)
    barcode_url = Column(String, nullable=True)
    barcode_value = Column(String, nullable=True)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business")
    category = relationship("Category") 

    @property
    def category_str(self):
        # Return user input first; fallback to relationship name
        return self.category_name or (self.category.name if self.category else None)
