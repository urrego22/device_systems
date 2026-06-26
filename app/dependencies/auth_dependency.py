from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.auth.security import decode_access_token
from app.models.user_model import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Usuario inactivo"
        )
    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Se requiere rol admin"
        )
    return current_user


def require_admin_or_support(
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=403,
            detail="Se requiere rol admin o support"
        )
    return current_user