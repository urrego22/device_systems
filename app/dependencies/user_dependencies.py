from fastapi import HTTPException, Header, Depends
from typing import Optional
from app.data.users_db import fake_db


def get_user_or_404(user_id: int) -> dict:
    """
    Dependencia reutilizable: busca un usuario por ID.
    Si no existe, lanza HTTPException 404 automáticamente.
    Se usa con Depends() en las rutas que necesiten el usuario por ID.
    """
    user = next((u for u in fake_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "message": f"Usuario con ID {user_id} no encontrado", "status_code": 404}
        )
    return user


def get_api_config() -> dict:
    """
    Dependencia: retorna configuración general de la API.
    Puede inyectarse en cualquier endpoint para acceder a estos valores.
    """
    return {
        "api_name": "device_systems API",
        "version": "2.0.0",
        "author": "Sara García"
    }


def verify_api_key(x_api_key: Optional[str] = Header(default=None)) -> dict:
    """
    Dependencia: simula autenticación básica mediante cabecera HTTP.
    Para pruebas usa la cabecera: X-API-Key: device-systems-2025
    Si no se envía clave, se permite el acceso en modo demo.
    """
    valid_key = "device-systems-2025"
    if x_api_key and x_api_key != valid_key:
        raise HTTPException(
            status_code=401,
            detail={"error": True, "message": "API Key inválida", "status_code": 401}
        )
    return {"authenticated": bool(x_api_key), "user": "sara_garcia" if x_api_key else "anonymous"}