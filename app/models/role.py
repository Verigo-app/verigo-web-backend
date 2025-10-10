from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base
from app.models.base import Base 

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)