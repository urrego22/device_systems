from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token
)


def register_user(db: Session, data: UserRegister):

    existing = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )

    allowed_roles = ["admin", "support", "user"]
    if data.role not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Rol no permitido. Usa: {allowed_roles}"
        )

    hashed = get_password_hash(data.password)

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hashed,
        role=data.role,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Usuario inactivo"
        )

    token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )

    return {"access_token": token, "token_type": "bearer"}