from pydantic import BaseModel, EmailStr
from datetime import datetime

# ================================
# CATEGORY SCHEMAS
# ================================

class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Para Pydantic V2


# ================================
# AUTH USER SCHEMA
# ================================

class AuthUser(BaseModel):
    email: EmailStr
    role: str | None = None
