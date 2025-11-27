from pydantic import BaseModel
from datetime import datetime

# ==========================
# CITY SCHEMAS
# ==========================

class CityBase(BaseModel):
    name: str
    country: str
    state: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityOut(CityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
