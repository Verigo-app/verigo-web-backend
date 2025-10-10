# app/utils/barcode.py
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO

def extract_barcode(file) -> str | None:
    file.file.seek(0)
    img = Image.open(BytesIO(file.file.read()))
    barcodes = decode(img)
    if barcodes:
        return barcodes[0].data.decode("utf-8")
    return None
