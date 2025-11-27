from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, schemas, crud, auth
from .auth import get_city  # ← IMPORTANTE


models.PointOfSale.metadata.create_all(bind=database.engine)

app = FastAPI(title="Points of Sale Microservice")


@app.get("/api/v1/points-of-sale")
def list_points_of_sale(db: Session = Depends(database.get_db)):
    all_pos = crud.get_all_pos(db)

    result = []
    for pos in all_pos:
        city = get_city(pos.city_id)
        result.append({
            **pos.__dict__,
            "city": city
        })

    return result


@app.get("/api/v1/points-of-sale/{pos_id}")
def read_pos(pos_id: int, db: Session = Depends(database.get_db)):
    pos = crud.get_pos(db, pos_id)
    if not pos:
        raise HTTPException(status_code=404, detail="Punto de venta no encontrado")

    city = get_city(pos.city_id)

    return {
        **pos.__dict__,
        "city": city
    }


@app.post("/api/v1/points-of-sale", response_model=schemas.POSOut, status_code=201)
def create_pos(
    pos: schemas.POSCreate,
    db: Session = Depends(database.get_db),
    _: auth.admin_required = Depends()
):
    # Validar ciudad contra ms-cities
    city = get_city(pos.city_id)

    if not city:
        raise HTTPException(
            status_code=400,
            detail=f"La ciudad con id {pos.city_id} no existe"
        )

    return crud.create_pos(db, pos)



@app.put("/api/v1/points-of-sale/{pos_id}", response_model=schemas.POSOut)
def update_pos(
    pos_id: int,
    pos: schemas.POSUpdate,
    db: Session = Depends(database.get_db),
    _: auth.admin_required = Depends()
):
    updated = crud.update_pos(db, pos_id, pos)
    if not updated:
        raise HTTPException(status_code=404, detail="Punto de venta no encontrado")
    return updated


@app.delete("/api/v1/points-of-sale/{pos_id}", status_code=204)
def delete_pos(
    pos_id: int,
    db: Session = Depends(database.get_db),
    _: auth.admin_required = Depends()
):
    deleted = crud.delete_pos(db, pos_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Punto de venta no encontrado")
