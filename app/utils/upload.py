# app/utils/upload.py
from cloudinary.uploader import upload

def upload_to_cloudinary(file) -> str:
    """
    Upload a file to Cloudinary and return the URL.
    `file` should be a file-like object from FastAPI UploadFile.
    """
    result = upload(file.file)
    return result.get("secure_url")
