# # app/api/profile.py
# from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
# from sqlalchemy.orm import Session
# from app.db.session import get_db
# from app.crud import mobile_profile as crud_profile
# from app.schemas.mobile.profile import ProfileOut, ProfileUpdate, ChangePassword
# from app.api.auth import get_current_user  # your JWT/Session auth dependency

# router = APIRouter(prefix="/profile", tags=["Profile"])

# @router.get("/", response_model=ProfileOut)
# def get_my_profile(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
#     user = crud_profile.get_profile(db, current_user.id)
#     return user

# @router.put("/", response_model=ProfileOut)
# def update_my_profile(updates: ProfileUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
#     user = crud_profile.update_profile(db, current_user.id, updates)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.post("/upload-picture", response_model=ProfileOut)
# def upload_profile_picture(file: UploadFile = File(...), current_user = Depends(get_current_user), db: Session = Depends(get_db)):
#     # Save the file somewhere and get URL
#     file_location = f"/static/profile_pics/{current_user.id}_{file.filename}"
#     with open(f"app{file_location}", "wb+") as f:
#         f.write(file.file.read())
    
#     user = crud_profile.update_profile_picture(db, current_user.id, file_location)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# @router.post("/change-password")
# def change_password(data: ChangePassword, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
#     success = crud_profile.change_password(db, current_user.id, data.old_password, data.new_password)
#     if success is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     if success is False:
#         raise HTTPException(status_code=400, detail="Old password is incorrect")
#     return {"message": "Password updated successfully"}
