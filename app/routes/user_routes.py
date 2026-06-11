from fastapi import APIRouter, status, Depends, Query
from typing import Optional, List
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services import user_service
from app.dependencies.database_dependency import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Filtra por rol, estado o cambia el orden.",
    response_description="Lista de usuarios registrados en base de datos"
)
def get_users(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support o user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado: true o false"),
    order_by: Optional[str] = Query("id", description="Ordenar por: id, name o created_at"),
    db: Session = Depends(get_db)
):
    return user_service.get_all_users(db, role=role, is_active=is_active, order_by=order_by)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Busca un usuario en la base de datos por su ID. Retorna 404 si no existe.",
    response_description="Datos del usuario encontrado"
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Crea un nuevo usuario en la base de datos. Valida correo único y rol permitido.",
    response_description="Usuario creado exitosamente"
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completamente (PUT)",
    description="Reemplaza todos los campos del usuario en la base de datos.",
    response_description="Usuario actualizado completamente"
)
def update_user_full(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user_full(db, user_id, user_data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente (PATCH)",
    description="Modifica solo los campos enviados. Body vacío retorna 400.",
    response_description="Usuario actualizado parcialmente"
)
def update_user_partial(user_id: int, user_data: UserPatch, db: Session = Depends(get_db)):
    return user_service.update_user_partial(db, user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario de la base de datos. Retorna 404 si no existe.",
    response_description="Usuario eliminado"
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)
    return None