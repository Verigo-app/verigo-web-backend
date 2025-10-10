# app/utils/upload.py
import cloudinary.uploader
from app.core.cloudinary_config import cloudinary

def upload_to_cloudinary(file) -> str:
    result = cloudinary.uploader.upload(file.file)
    return result.get("secure_url")
