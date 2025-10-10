from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from app.db.session import get_db
from app.crud import product as crud_product
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.models.user import User
from app.models.business import Business
from app.models.product import Product
from app.models.category import Category
from app.utils.upload import upload_to_cloudinary
from app.utils.barcode import extract_barcode

router = APIRouter(prefix="/product", tags=["Product"])


# ================= CREATE PRODUCT =================
@router.post("/", response_model=ProductOut, summary="Create a product")
def create_product(
    name: str = Form(...),
    description: str | None = Form(None),
    category_name: str = Form(...),
    product_image: UploadFile = File(...),
    barcode_image: UploadFile = File(None),
    business_id: int | None = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name != "business":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only business users can create products"
        )

    # ✅ Fetch category by name
    category = db.query(Category).filter(Category.name.ilike(category_name)).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category '{category_name}' not found")

    # ✅ Determine business
    if business_id:
        business = db.query(Business).filter(
            Business.id == business_id,
            Business.user_id == current_user.id
        ).first()
        if not business:
            raise HTTPException(status_code=404, detail="Business not found or not owned by user")
    else:
        businesses = db.query(Business).filter(Business.user_id == current_user.id).all()
        if not businesses:
            raise HTTPException(status_code=400, detail="User does not have a registered business")
        elif len(businesses) == 1:
            business = businesses[0]
        else:
            raise HTTPException(
                status_code=400,
                detail="Multiple businesses found, please specify business_id"
            )

    # ✅ Upload product image
    pic_url = upload_to_cloudinary(product_image)

    barcode_url, barcode_value, verified = None, None, False
    if barcode_image:
        barcode_url = upload_to_cloudinary(barcode_image)
        barcode_value = extract_barcode(barcode_image)
        verified = bool(barcode_value)

    # ✅ Create product
    product_data = ProductCreate(
        name=name,
        description=description,
        pic_url=pic_url,
        barcode_url=barcode_url,
        barcode_value=barcode_value,
        verified=verified
    )

    db_product = crud_product.create_product(db, business.id, product_data)
    db_product.category_id = category.id
    db_product.category_name = category.name
    db.commit()
    db.refresh(db_product)

    return db_product


# ================= UPDATE PRODUCT =================
@router.put("/{product_id}", response_model=ProductOut, summary="Update a product")
def update_product(
    product_id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    category_name: str | None = Form(None),
    product_image: UploadFile | None = File(None),
    barcode_image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.business.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = ProductUpdate()

    if name is not None:
        update_data.name = name
    if description is not None:
        update_data.description = description

    # ✅ Update category by name
    if category_name:
        category = db.query(Category).filter(Category.name.ilike(category_name)).first()
        if not category:
            raise HTTPException(status_code=404, detail=f"Category '{category_name}' not found")
        product.category_id = category.id
        product.category_name = category.name

    if product_image:
        update_data.pic_url = upload_to_cloudinary(product_image)

    if barcode_image:
        update_data.barcode_url = upload_to_cloudinary(barcode_image)
        update_data.barcode_value = extract_barcode(barcode_image)
        update_data.verified = bool(update_data.barcode_value)

    return crud_product.update_product(db, product_id, update_data)
