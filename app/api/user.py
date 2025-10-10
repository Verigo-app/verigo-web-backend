# app/api/user.py
from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(tags=["Users"])

@router.get("/me", response_model=UserOut, summary="Get current logged-in user")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
