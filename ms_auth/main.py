from fastapi import FastAPI
from sqlalchemy.orm import Session

# Imports relativos
from . import models, database, routes
from .database import engine
from .models import Base
from .utils import hash_password
from .routes import router


# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Authentication Microservice")

# Incluir las rutas
app.include_router(router)


# Crear admin inicial si no existe (solo en desarrollo)
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
