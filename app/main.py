# app/main.py
from fastapi import FastAPI
from app.api import auth, user,business, product, promotion
from app.api.mobile import home as mobile_home
from app.api.mobile import scan as barcode_router
from app.api.mobile import profile as mobile_profile

app = FastAPI(title="Verigo Backend")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(business.router, prefix="/business")
app.include_router(product.router, prefix="/product")
app.include_router(promotion.router, prefix="/promotion")
app.include_router(mobile_home.router)
app.include_router(barcode_router.router)
# app.include_router(mobile_profile.router)







































































