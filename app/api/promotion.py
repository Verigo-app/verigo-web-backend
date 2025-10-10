# app/api/promotion.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import promotion as crud_promo
from app.schemas.promotion import PromotionCreate, PromotionOut, PromotionUpdate
from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter(prefix="/promotion", tags=["Promotion"])

@router.post("/", response_model=PromotionOut)
def create_promotion(
    promotion: PromotionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name != "business":
        raise HTTPException(status_code=403, detail="Only business users can create promotions")
    # assume one business per user for now
    business_id = current_user.businesses[0].id
    return crud_promo.create_promotion(db, business_id, promotion)

@router.get("/", response_model=list[PromotionOut])
def list_promotions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    business_id = current_user.businesses[0].id
    return crud_promo.list_promotions(db, business_id)

@router.get("/{promotion_id}", response_model=PromotionOut)
def get_promotion(promotion_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    promo = crud_promo.get_promotion(db, promotion_id)
    if not promo:
        raise HTTPException(404, "Promotion not found")
    if promo.business_id not in [b.id for b in current_user.businesses]:
        raise HTTPException(403, "Not authorized")
    return promo

@router.put("/{promotion_id}", response_model=PromotionOut)
def update_promotion(promotion_id: int, promotion: PromotionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    promo = crud_promo.get_promotion(db, promotion_id)
    if not promo:
        raise HTTPException(404, "Promotion not found")
    if promo.business_id not in [b.id for b in current_user.businesses]:
        raise HTTPException(403, "Not authorized")
    return crud_promo.update_promotion(db, promotion_id, promotion)

@router.delete("/{promotion_id}")
def delete_promotion(promotion_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    promo = crud_promo.get_promotion(db, promotion_id)
    if not promo:
        raise HTTPException(404, "Promotion not found")
    if promo.business_id not in [b.id for b in current_user.businesses]:
        raise HTTPException(403, "Not authorized")
    crud_promo.delete_promotion(db, promotion_id)
    return {"detail": "Promotion deleted successfully"}
