from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserVerify, UserLogin, UserOut, UserResend
from app.crud import user as crud_user
from app.core.security import create_access_token
from app.utils.email import send_verification_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserOut, summary="Register new user")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db),
    platform: str = Query("mobile", description="Specify platform: 'mobile' or 'web'")
):
    """
    User signup with platform-specific role:
    - mobile → customer
    - web → business
    """
    role_name = "customer" if platform.lower() == "mobile" else "business"
    db_user, code = crud_user.create_user(db, user, role_name)
    send_verification_email(db_user.email, code)

    return UserOut(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        role=db_user.role.name,
        is_verified=db_user.is_verified,
        created_at=db_user.created_at
    )


@router.post("/verify", response_model=UserOut, summary="Verify user account")
def verify_account(data: UserVerify, db: Session = Depends(get_db)):
    user = crud_user.verify_user(db, data.email, data.code)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification code")
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role.name,
        is_verified=user.is_verified,
        created_at=user.created_at
    )


@router.post("/login", summary="User login and JWT token")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user == "not_verified":
        raise HTTPException(status_code=403, detail="Account not verified")

    token = create_access_token({"sub": user.email, "role": user.role.name})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/resend-code", summary="Resend verification code")
def resend_code(data: UserResend, db: Session = Depends(get_db)):
    user_data = crud_user.resend_verification_code(db, data.email)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    if user_data == "already_verified":
        raise HTTPException(status_code=400, detail="User is already verified")

    user, code = user_data
    send_verification_email(user.email, code)
    return {"message": f"Verification code resent to {user.email}"}
