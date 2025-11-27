from sqlalchemy.orm import Session
from . import models, schemas


def get_pos(db: Session, pos_id: int):
    return db.query(models.PointOfSale).filter(models.PointOfSale.id == pos_id).first()


def get_all_pos(db: Session):
    return db.query(models.PointOfSale).all()


def create_pos(db: Session, pos: schemas.POSCreate):
    db_pos = models.PointOfSale(**pos.model_dump())
    db.add(db_pos)
    db.commit()
    db.refresh(db_pos)
    return db_pos


def update_pos(db: Session, pos_id: int, pos: schemas.POSUpdate):
    db_pos = get_pos(db, pos_id)
    if not db_pos:
        return None

    for key, value in pos.model_dump(exclude_unset=True).items():
        setattr(db_pos, key, value)

    db.commit()
    db.refresh(db_pos)
    return db_pos


def delete_pos(db: Session, pos_id: int):
    db_pos = get_pos(db, pos_id)
    if not db_pos:
        return None

    db.delete(db_pos)
    db.commit()
    return True

def get_all_pos(db: Session):
    return db.query(models.PointOfSale).all()
