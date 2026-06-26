from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.schemas.user_schema import UserResponse
from app.auth import auth_service
from app.rate_limiter import limiter


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    summary="Registrar usuario",
    description="Crea un usuario nuevo con contraseña segura hasheada."
)
@limiter.limit("3/minute")
def register(
    request: Request,
    data: UserRegister,
    db: Session = Depends(get_db)
):
    return auth_service.register_user(db, data)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica el usuario y retorna un token JWT."
)
@limiter.limit("5/minute")
def login(
    request: Request,
    data: UserLogin,
    db: Session = Depends(get_db)
):
    return auth_service.login_user(db, data.email, data.password)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Usuario autenticado",
    description="Retorna los datos del usuario autenticado sin mostrar la contraseña."
)
def me(
    current_user=Depends(get_current_active_user)
):
    return current_user