from fastapi import HTTPException
from app.data.users_db import fake_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserPartialUpdate


def get_all_users(role=None, is_active=None):
    result = fake_db
    if role:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result


def get_user_by_id(user_id: int):
    user = next((u for u in fake_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "message": f"Usuario con ID {user_id} no encontrado", "status_code": 404}
        )
    return user


def create_user(user_data: UserCreate):
    if any(u["email"] == user_data.email for u in fake_db):
        raise HTTPException(
            status_code=400,
            detail={"error": True, "message": "El correo ya está registrado", "status_code": 400}
        )
    new_id = max(u["id"] for u in fake_db) + 1 if fake_db else 1
    new_user = {
        "id": new_id,
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role,
        "is_active": user_data.is_active
    }
    fake_db.append(new_user)
    return new_user


def update_user_full(user_id: int, user_data: UserUpdate):
    user = get_user_by_id(user_id)
    # Validar correo duplicado ignorando el propio usuario
    for u in fake_db:
        if u["email"] == user_data.email and u["id"] != user_id:
            raise HTTPException(
                status_code=400,
                detail={"error": True, "message": "El correo ya está en uso por otro usuario", "status_code": 400}
            )
    user["name"] = user_data.name
    user["email"] = user_data.email
    user["role"] = user_data.role
    user["is_active"] = user_data.is_active
    return user


def update_user_partial(user_id: int, user_data: UserPartialUpdate):
    user = get_user_by_id(user_id)
    fields = user_data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "message": "Debes enviar al menos un campo para actualizar", "status_code": 400}
        )
    # Validar correo duplicado si se envió email
    if "email" in fields:
        for u in fake_db:
            if u["email"] == fields["email"] and u["id"] != user_id:
                raise HTTPException(
                    status_code=400,
                    detail={"error": True, "message": "El correo ya está en uso", "status_code": 400}
                )
    user.update(fields)
    return user


def delete_user(user_id: int):
    user = get_user_by_id(user_id)
    fake_db.remove(user)