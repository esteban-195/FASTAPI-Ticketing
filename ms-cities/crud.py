from sqlalchemy.orm import Session
from . import models, schemas

def get_city(db: Session, city_id: int):
    return db.query(models.City).filter(models.City.id == city_id).first()

def get_cities(db: Session):
    return db.query(models.City).all()

def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def update_city(db: Session, city_id: int, city: schemas.CityUpdate):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        return None

    for key, value in city.model_dump(exclude_unset=True).items():
        setattr(db_city, key, value)

    db.commit()
    db.refresh(db_city)
    return db_city

def delete_city(db: Session, city_id: int):
    db_city = db.query(models.City).filter(models.City.id == city_id).first()
    if not db_city:
        return None
    db.delete(db_city)
    db.commit()
    return True
