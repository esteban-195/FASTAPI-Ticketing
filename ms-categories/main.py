from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import database, models, schemas, crud, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Categories Microservice")

@app.get("/categories", response_model=list[schemas.CategoryOut])
def read_categories(db: Session = Depends(database.get_db)):
    return crud.get_categories(db)

@app.get("/categories/{category_id}", response_model=schemas.CategoryOut)
def read_category(category_id: int, db: Session = Depends(database.get_db)):
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@app.post("/categories", response_model=schemas.CategoryOut, status_code=201)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(database.get_db),
                    _: auth.admin_required = Depends()):
    return crud.create_category(db, category)

@app.put("/categories/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, category: schemas.CategoryUpdate,
                    db: Session = Depends(database.get_db), _: auth.admin_required = Depends()):
    updated = crud.update_category(db, category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return updated

@app.delete("/categories/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(database.get_db), _: auth.admin_required = Depends()):
    deleted = crud.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
