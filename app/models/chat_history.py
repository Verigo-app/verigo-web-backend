from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String, Boolean, Float, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
