from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    state = Column(String(120), nullable=True)
    country = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
