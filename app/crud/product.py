# app/crud/product.py
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, business_id: int, product: ProductCreate):
    db_product = Product(
        business_id=business_id,
        name=product.name,
        description=product.description,
        pic_url=product.pic_url,
        barcode_url=product.barcode_url,
        barcode_value=product.barcode_value,
        verified=product.verified
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    for field, value in product.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products_by_business(db: Session, business_id: int):
    return db.query(Product).filter(Product.business_id == business_id).all()
