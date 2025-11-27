from fastapi import FastAPI
from . import models, database, routes  # importa tus rutas existentes
import os

# Crear las tablas si no existen
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Authentication Microservice")

# Incluir tus rutas
app.include_router(routes.router)

# Crear admin inicial si no existe (opcional, para pruebas)
from sqlalchemy.orm import Session
from .utils import hash_password

def create_admin():
    db: Session = next(database.get_db())
    from .models import User
    if not db.query(User).filter(User.role == "admin").first():
        admin = User(
            name="Admin",
            email="admin@admin.com",
            hashed_password=hash_password("123"),
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("Admin creado: admin@admin.com / 123")

create_admin()
