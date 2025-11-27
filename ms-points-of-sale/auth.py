from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
import requests
import os
load_dotenv(dotenv_path="ms-points-of-sale/.env")

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

CITIES_URL = os.getenv("CITIES_SERVICE_URL", "http://127.0.0.1:8003/api/v1")


def get_city(city_id: int):
    response = requests.get(f"{CITIES_URL}/cities/{city_id}")
    print(">>> URL:", f"{CITIES_URL}/cities/{city_id}")
    print(">>> STATUS:", response.status_code)
    print(">>> BODY:", response.text)
    if response.status_code == 200:
        return response.json()
    return None


def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        role = payload.get("role")

        if not email:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        return {"email": email, "role": role}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


def admin_required(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado. Se requiere el rol de Administrador."
        )
    return current_user
