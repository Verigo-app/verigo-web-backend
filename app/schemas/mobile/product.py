from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    pic_url: Optional[str]
    # Here we accept Category object but return only its name
    category: Optional[str] = None  

    average_rating: Optional[float] = 0.0
    total_views: Optional[int] = 0
    total_scans: Optional[int] = 0
    is_verified: Optional[bool] = False
    promotion_title: Optional[str] = None
    promotion_discount: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, obj):
        # Extract category name if Category object exists
        category_name = None
        if hasattr(obj, "category") and obj.category:
            category_name = obj.category.name
        return cls(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            pic_url=obj.pic_url,
            category=category_name,
            average_rating=getattr(obj, "average_rating", 0.0),
            total_views=getattr(obj, "total_views", 0),
            total_scans=getattr(obj, "total_scans", 0),
            is_verified=getattr(obj, "verified", False),
            promotion_title=getattr(obj, "promotion_title", None),
            promotion_discount=getattr(obj, "promotion_discount", None),
        )
