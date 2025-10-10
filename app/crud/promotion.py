# app/crud/promotion.py
from sqlalchemy.orm import Session
from app.models.promotion import Promotion
from app.schemas.promotion import PromotionCreate, PromotionUpdate

def create_promotion(db: Session, business_id: int, promotion: PromotionCreate):
    db_promo = Promotion(**promotion.dict(), business_id=business_id)
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)
    return db_promo

def get_promotion(db: Session, promotion_id: int):
    return db.query(Promotion).filter(Promotion.id == promotion_id).first()

def list_promotions(db: Session, business_id: int):
    return db.query(Promotion).filter(Promotion.business_id == business_id).all()

def update_promotion(db: Session, promotion_id: int, promotion: PromotionUpdate):
    db_promo = get_promotion(db, promotion_id)
    if not db_promo:
        return None
    for key, value in promotion.dict(exclude_unset=True).items():
        setattr(db_promo, key, value)
    db.commit()
    db.refresh(db_promo)
    return db_promo

def delete_promotion(db: Session, promotion_id: int):
    db_promo = get_promotion(db, promotion_id)
    if not db_promo:
        return None
    db.delete(db_promo)
    db.commit()
    return True
