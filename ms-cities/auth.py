from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="ms-cities/.env")

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


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
