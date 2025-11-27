from pydantic import BaseModel, Field, validator
from datetime import datetime


class POSBase(BaseModel):
    name: str
    address: str
    city_id: int
    phone: str | None = None
    is_active: bool = True

    @validator("city_id")
    def validar_city_id(cls, v):
        if v <= 0:
            raise ValueError("El ID de ciudad debe ser mayor que cero.")
        return v

class POSCreate(POSBase):
    pass


class POSUpdate(POSBase):
    pass


class POSOut(POSBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
