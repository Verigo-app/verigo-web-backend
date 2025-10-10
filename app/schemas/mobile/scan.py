# app/schemas/scan.py
from pydantic import BaseModel
from typing import Optional, Dict

class BarcodeScanResponse(BaseModel):
    verified: bool
    message: str
    redirect_url: Optional[str] = None
    product: Optional[Dict] = None
