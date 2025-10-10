from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    role = relationship("Role")

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    brand_name = Column(String)
    category = Column(String)  # ✅ Added
    picture_url = Column(String)  # ✅ Added
    address = Column(String)  # ✅ Added
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    name = Column(String)
    description = Column(Text)
    pic_url = Column(String)
    barcode_url = Column(String, nullable=True)
    barcode_value = Column(String, nullable=True)
    verified = Column(Boolean, default=False)  # ✅ Optional barcode → verification
    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business")

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

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ChatResponse(Base):
    __tablename__ = "chat_response"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Analysis(Base):
    __tablename__ = "analysis"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    feedback = Column(Text)
    rating = Column(Integer)
    views = Column(Integer, default=0)  # ✅ Added
    scans = Column(Integer, default=0)  # ✅ Added
    created_at = Column(DateTime, default=datetime.utcnow)