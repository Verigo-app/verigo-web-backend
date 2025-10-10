import random
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.core.security import get_password_hash, verify_password


def create_user(db: Session, user_data, role_name: str):
    """Create a new user with a verification code."""
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise ValueError(f"Role '{role_name}' does not exist")

    code = str(random.randint(100000, 999999))
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role_id=role.id,
        is_verified=False,
        verification_code=code
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user, code


def verify_user(db: Session, email: str, code: str):
    """Verify user using email + verification code"""
    db_user = db.query(User).filter(User.email == email).first()
    if db_user and db_user.verification_code == code:
        db_user.is_verified = True
        db_user.verification_code = None
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def authenticate_user(db: Session, email: str, password: str):
    """Authenticate user with email and password"""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    if not user.is_verified:
        return "not_verified"
    return user


def resend_verification_code(db: Session, email: str):
    """Resend verification code if user not verified"""
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        return None
    if db_user.is_verified:
        return "already_verified"

    code = str(random.randint(100000, 999999))
    db_user.verification_code = code
    db.commit()
    db.refresh(db_user)
    return db_user, code
