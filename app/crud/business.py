# app/crud/business.py
from sqlalchemy.orm import Session
from app.models.business import Business
from app.schemas.business import BusinessCreate, BusinessUpdate

def create_business(db: Session, user_id: int, business: BusinessCreate):
    db_business = Business(
        user_id=user_id,
        brand_name=business.brand_name,
        category=business.category,
        picture_url=business.picture_url,
        address=business.address,
        description=business.description
    )
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business

def update_business(db: Session, business_id: int, data: BusinessUpdate):
    db_business = db.query(Business).filter(Business.id == business_id).first()
    if not db_business:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_business, field, value)
    db.commit()
    db.refresh(db_business)
    return db_business

def get_business_by_user(db: Session, user_id: int):
    return db.query(Business).filter(Business.user_id == user_id).all()

def get_business(db: Session, business_id: int):
    return db.query(Business).filter(Business.id == business_id).first()
