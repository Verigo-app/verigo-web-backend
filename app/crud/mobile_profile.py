# # app/crud/mobile_profile.py
# from sqlalchemy.orm import Session
# from app.models.user import User
# from app.schemas.mobile.profile import ProfileUpdate

# def get_profile(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()

# def update_profile(db: Session, user_id: int, updates: ProfileUpdate):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         return None
#     for field, value in updates.dict(exclude_unset=True).items():
#         setattr(user, field, value)
#     db.commit()
#     db.refresh(user)
#     return user

# def update_profile_picture(db: Session, user_id: int, profile_pic_url: str):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         return None
#     user.profile_pic = profile_pic_url
#     db.commit()
#     db.refresh(user)
#     return user

# def change_password(db: Session, user_id: int, old_password: str, new_password: str):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         return None
#     if not user.verify_password(old_password):  # assuming User model has this method
#         return False
#     user.set_password(new_password)  # assuming User model has this method
#     db.commit()
#     return True
