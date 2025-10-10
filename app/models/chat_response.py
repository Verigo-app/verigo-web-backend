from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String, Boolean, Float, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class ChatResponse(Base):
    __tablename__ = "chat_response"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
