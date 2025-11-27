from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, schemas, crud, auth

models.City.metadata.create_all(bind=database.engine)

app = FastAPI(title="Cities Microservice")


@app.get("/api/v1/cities", response_model=list[schemas.CityOut])
def read_cities(db: Session = Depends(database.get_db)):
    return crud.get_cities(db)


@app.get("/api/v1/cities/{city_id}", response_model=schemas.CityOut)
def read_city(city_id: int, db: Session = Depends(database.get_db)):
    city = crud.get_city(db, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return city


@app.post("/api/v1/cities", response_model=schemas.CityOut, status_code=201)
def create_city(
    city: schemas.CityCreate,
    db: Session = Depends(database.get_db),
    _: auth.admin_required = Depends()
):
    return crud.create_city(db, city)


@app.put("/api/v1/cities/{city_id}", response_model=schemas.CityOut)
def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: Session = Depends(database.get_db),
    _: auth.admin_required = Depends()
):
    updated = crud.update_city(db, city_id, city)
    if not updated:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
    return updated


@app.delete("/api/v1/cities/{city_id}", status_code=204)
def delete_city(
    city_id: int,
    db: Session = Depends(database.get_db),
    _: auth.admin_required = Depends()
):
    deleted = crud.delete_city(db, city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ciudad no encontrada")
