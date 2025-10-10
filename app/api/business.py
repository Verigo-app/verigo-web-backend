# app/api/business.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.business import BusinessCreate, BusinessUpdate, BusinessOut
from app.crud import business as crud_business
from app.core.deps import get_current_user
from app.db.session import get_db 
from app.models.user import User

router = APIRouter(prefix="/business", tags=["Business"])

# Create business
@router.post("/", response_model=BusinessOut, summary="Register a business")
def register_business(
    business: BusinessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only business users can register a business
    if current_user.role.name != "business":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only business users can register a business"
        )
    return crud_business.create_business(db, current_user.id, business)

# Update business
@router.put("/{business_id}", response_model=BusinessOut, summary="Update business info")
def update_business(
    business_id: int,
    business: BusinessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_business = crud_business.get_business(db, business_id)
    if not db_business or db_business.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Business not found")
    return crud_business.update_business(db, business_id, business)

# Get my businesses
@router.get("/my-businesses", response_model=list[BusinessOut], summary="Get current user's businesses")
def get_my_businesses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_business.get_business_by_user(db, current_user.id)
