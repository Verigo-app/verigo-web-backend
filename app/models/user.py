# app/models/user.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    is_verified = Column(Boolean, default=False)  # ✅ keep for email verification
    verification_code = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role", backref="users")
    businesses = relationship("Business", back_populates="owner")
