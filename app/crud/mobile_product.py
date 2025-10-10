from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.product import Product
from app.models.category import Category
from app.models.promotion import Promotion
from app.models.analytics import Analysis
from typing import List, Tuple

def create_product(db: Session, name: str, description: str, pic_url: str, category_name: str, business_id: int):
    category = db.query(Category).filter(Category.name.ilike(category_name)).first()
    if not category:
        category = Category(name=category_name)
        db.add(category)
        db.commit()
        db.refresh(category)

    product = Product(
        name=name,
        description=description,
        pic_url=pic_url,
        category_id=category.id,
        business_id=business_id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_products_by_name(db: Session, name: str) -> List[Product]:
    return db.query(Product).options(joinedload(Product.category)).filter(Product.name.ilike(f"%{name}%")).all()

def get_products_by_category(db: Session, category_name: str) -> List[Product]:
    return db.query(Product).join(Category).options(joinedload(Product.category)).filter(Category.name.ilike(category_name)).all()

def get_products_with_promotions(db: Session) -> List[Tuple[Product, Promotion]]:
    return (
        db.query(Product, Promotion)
        .join(Promotion, Product.id == Promotion.product_id)
        .options(joinedload(Product.category))
        .all()
    )

def get_new_products(db: Session) -> List[Product]:
    return db.query(Product).options(joinedload(Product.category)).order_by(Product.id.desc()).limit(20).all()

def get_popular_products(db: Session):
    subquery = (
        db.query(
            Analysis.product_id,
            func.count(Analysis.id).label("scan_count")
        )
        .group_by(Analysis.product_id)
        .subquery()
    )

    products = (
        db.query(Product, func.coalesce(subquery.c.scan_count, 0).label("scan_count"))
        .outerjoin(subquery, Product.id == subquery.c.product_id)
        .order_by(func.coalesce(subquery.c.scan_count, 0).desc())
        .limit(20)
        .all()
    )

    # Only return Product objects, ignore scan_count for response
    return [p[0] for p in products]

def get_most_viewed_products(db: Session):
    subquery = (
        db.query(
            Analysis.product_id,
            func.sum(Analysis.views).label("view_count")  # <- use correct column
        )
        .group_by(Analysis.product_id)
        .subquery()
    )

    products = (
        db.query(Product, func.coalesce(subquery.c.view_count, 0).label("view_count"))
        .outerjoin(subquery, Product.id == subquery.c.product_id)
        .order_by(func.coalesce(subquery.c.view_count, 0).desc())
        .limit(20)
        .all()
    )

    return [p[0] for p in products]
