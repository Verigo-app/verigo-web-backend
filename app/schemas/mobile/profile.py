# # app/schemas/mobile/profile.py
# from pydantic import BaseModel, ConfigDict, EmailStr
# from typing import Optional

# class ProfileOut(BaseModel):
#     id: int
#     name: str
#     email: EmailStr
#     phone: Optional[str] = None
#     profile_pic: Optional[str] = None

#     model_config = ConfigDict(from_attributes=True)

# class ProfileUpdate(BaseModel):
#     name: Optional[str] = None
#     phone: Optional[str] = None
#     email: Optional[EmailStr] = None

# class ChangePassword(BaseModel):
#     old_password: str
#     new_password: str
