# app/utils/create_db.py
from app.models.base import Base
from app.db.session import engine

# 1. Users first (FK for Business)
from app.models.user import User

# 2. Business depends on Users
from app.models.business import Business

# 3. Product depends on Business
from app.models.product import Product

# 4. Chat tables depend on Product/Business
from app.models.chat_history import ChatHistory
from app.models.chat_response import ChatResponse

# 5. Any remaining models (Role, Analytics, Promotion)
from app.models.role import Role
from app.models.analytics import Analysis
from app.models.promotion import Promotion

print("Creating tables in Neon...")
Base.metadata.create_all(bind=engine)
print("✅ Done! All tables created successfully.")
