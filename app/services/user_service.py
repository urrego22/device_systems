from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


def get_all_users(db: Session, role: str = None, is_active: bool = None, order_by: str = "id"):
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if order_by == "name":
        query = query.order_by(User.name)
    elif order_by == "created_at":
        query = query.order_by(User.created_at)
    else:
        query = query.order_by(User.id)

    return query.all()


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={"error": True, "message": f"Usuario con ID {user_id} no encontrado", "status_code": 404}
        )
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate):
    # Validar correo duplicado
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=400,
            detail={"error": True, "message": f"El correo '{user_data.email}' ya está registrado", "status_code": 400}
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user_full(db: Session, user_id: int, user_data: UserUpdate):
    user = get_user_by_id(db, user_id)

    # Validar correo duplicado ignorando el propio usuario
    existing = get_user_by_email(db, user_data.email)
    if existing and existing.id != user_id:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "message": f"El correo '{user_data.email}' ya está en uso", "status_code": 400}
        )

    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)
    return user


def update_user_partial(db: Session, user_id: int, user_data: UserPatch):
    user = get_user_by_id(db, user_id)

    fields = user_data.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(
            status_code=400,
            detail={"error": True, "message": "Debes enviar al menos un campo para actualizar", "status_code": 400}
        )

    if "email" in fields:
        existing = get_user_by_email(db, fields["email"])
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=400,
                detail={"error": True, "message": f"El correo '{fields['email']}' ya está en uso", "status_code": 400}
            )

    for key, value in fields.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()