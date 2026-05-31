from fastapi import APIRouter, status, Depends, Query, Response
from typing import Optional, List
from app.schemas.user_schema import UserCreate, UserUpdate, UserPartialUpdate, UserResponse
from app.services import user_service
from app.dependencies.user_dependencies import get_user_or_404, get_api_config

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los usuarios",
    description="Retorna todos los usuarios. Filtra opcionalmente por rol o estado activo/inactivo.",
    response_description="Lista de usuarios del sistema"
)
def get_users(
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support o user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado: true o false"),
    config: dict = Depends(get_api_config)
):
    return user_service.get_all_users(role=role, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuario por ID",
    description="Busca y retorna un usuario por su ID. Si no existe, responde 404.",
    response_description="Datos del usuario encontrado"
)
def get_user(user: dict = Depends(get_user_or_404)):
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo usuario",
    description="Crea un usuario nuevo. Valida que el correo no esté duplicado y que el rol sea válido.",
    response_description="Usuario creado exitosamente"
)
def create_user(user_data: UserCreate):
    return user_service.create_user(user_data)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario completamente (PUT)",
    description="Reemplaza TODOS los campos del usuario. Se deben enviar todos los campos obligatoriamente.",
    response_description="Usuario actualizado completamente"
)
def update_user_full(user_id: int, user_data: UserUpdate):
    return user_service.update_user_full(user_id, user_data)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario parcialmente (PATCH)",
    description="Modifica solo los campos enviados. Si envías un body vacío, responde 400.",
    response_description="Usuario actualizado parcialmente"
)
def update_user_partial(user_id: int, user_data: UserPartialUpdate):
    return user_service.update_user_partial(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario por su ID. Si no existe, responde 404.",
    response_description="Usuario eliminado (sin contenido en la respuesta)"
)
def delete_user(user_id: int, user: dict = Depends(get_user_or_404)):
    user_service.delete_user(user_id)
    return None