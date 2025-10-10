# app/api/scan.py
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.product import Product
from app.schemas.mobile.scan import BarcodeScanResponse
from PIL import Image
from pyzbar.pyzbar import decode
import io

router = APIRouter(prefix="/barcode", tags=["Barcode"])

# Internal helper function
def extract_barcode_and_lookup(file: UploadFile, db: Session) -> BarcodeScanResponse:
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes))
    
    barcodes = decode(image)
    if not barcodes:
        return BarcodeScanResponse(
            verified=False,
            message="No barcode detected. Try again."
        )
    
    barcode_number = barcodes[0].data.decode("utf-8")
    product = db.query(Product).filter(Product.barcode_value == barcode_number).first()
    
    if product:
        return BarcodeScanResponse(
            verified=True,
            message="Product verified!",
            redirect_url=f"/product/{product.id}",
            product={
                "id": product.id,
                "name": product.name,
                "pic_url": product.pic_url,
                "chatbot_url": f"/chatbot/product/{product.id}"
            }
        )
    
    return BarcodeScanResponse(
        verified=False,
        message="Product not verified or not found. Try searching by name."
    )

# --- Camera scan endpoint ---
@router.post("/camera-scan", response_model=BarcodeScanResponse)
def camera_scan(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Scan barcode using camera picture.
    """
    return extract_barcode_and_lookup(file, db)

# --- Upload image endpoint ---
@router.post("/upload-scan", response_model=BarcodeScanResponse)
def upload_scan(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Scan barcode from uploaded image file.
    """
    return extract_barcode_and_lookup(file, db)
