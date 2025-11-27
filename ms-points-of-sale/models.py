from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
from datetime import datetime


class PointOfSale(Base):
    __tablename__ = "points_of_sale"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    address = Column(String(255), nullable=False)
    city_id = Column(Integer, nullable=False)  # referencia lógica, no FK
    phone = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
