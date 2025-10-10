# app/models/business.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    brand_name = Column(String)
    category = Column(String)
    picture_url = Column(String)
    address = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User")

