from fastapi import APIRouter, HTTPException, Query, Response
from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

# Base de datos simulada en memoria
fake_db: List[dict] = [
    {"id": 1, "name": "Ana Torres", "email": "ana@mail.com",
     "role": "admin", "is_active": True},
    {"id": 2, "name": "Carlos López", "email": "carlos@mail.com",
     "role": "support", "is_active": True},
    {"id": 3, "name": "María Pérez", "email": "maria@mail.com",
     "role": "user", "is_active": False},
]


@router.get("/users", response_model=List[UserResponse])
def get_users(
    response: Response,
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    result = fake_db
    if role:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    user = next((u for u in fake_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"
    if any(u["email"] == user.email for u in fake_db):
        raise HTTPException(status_code=400,
                            detail="El correo ya está registrado")
    new_id = max(u["id"] for u in fake_db) + 1 if fake_db else 1
    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }
    fake_db.append(new_user)
    return new_user