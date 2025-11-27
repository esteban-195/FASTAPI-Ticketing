import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar .env (busca primero en el microservicio, si no está, usa el externo)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    load_dotenv()  # Busca .env externo

# URL de la DB
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///./users.db")

# Engine de SQLAlchemy (check_same_thread necesario para SQLite y FastAPI multithread)
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base declarativa
Base = declarative_base()

# Dependencia para endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
