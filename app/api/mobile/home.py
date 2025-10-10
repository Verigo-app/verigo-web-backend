from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import mobile_product
from app.schemas.mobile.product import ProductOut
from typing import List

router = APIRouter(prefix="/mobile/products", tags=["Mobile Products"])

def map_product(p):
    """Helper to convert SQLAlchemy Product -> ProductOut with category name."""
    return ProductOut(
        id=p.id,
        name=p.name,
        description=p.description,
        pic_url=p.pic_url,
        category=p.category.name if p.category else None,
        average_rating=getattr(p, "average_rating", 0.0),
        total_views=getattr(p, "total_views", 0),
        total_scans=getattr(p, "total_scans", 0),
        is_verified=p.verified,
        promotion_title=getattr(p, "promotion_title", None),
        promotion_discount=getattr(p, "promotion_discount", None),
    )

@router.get("/search", response_model=List[ProductOut])
def search_products(name: str, db: Session = Depends(get_db)):
    products = mobile_product.get_products_by_name(db, name)
    return [map_product(p) for p in products]

@router.get("/view-by-category/{category_name}", response_model=List[ProductOut])
def products_by_category(category_name: str, db: Session = Depends(get_db)):
    products = mobile_product.get_products_by_category(db, category_name)
    return [map_product(p) for p in products]

@router.get("/product-promotions", response_model=List[ProductOut])
def products_with_promotions(db: Session = Depends(get_db)):
    results = mobile_product.get_products_with_promotions(db)
    products_out = []
    for product, promo in results:
        p_out = map_product(product)
        p_out.promotion_title = promo.title
        p_out.promotion_discount = promo.discount_percent
        products_out.append(p_out)
    return products_out

@router.get("/p-new-products", response_model=List[ProductOut])
def new_products(db: Session = Depends(get_db)):
    products = mobile_product.get_new_products(db)
    return [map_product(p) for p in products]

@router.get("/p-popular", response_model=List[ProductOut])
def popular_products(db: Session = Depends(get_db)):
    products = mobile_product.get_popular_products(db)
    return [map_product(p) for p in products]

@router.get("/most-viewed", response_model=List[ProductOut])
def most_viewed_products(db: Session = Depends(get_db)):
    products = mobile_product.get_most_viewed_products(db)
    return [map_product(p) for p in products]
