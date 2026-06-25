from sqlalchemy.orm import Session

from app.models.user_model import User

from app.schemas.auth_schema import (
    UserRegister,
    UserLogin
)

from app.auth.security import (
    get_password_hash,
    verify_password,
    create_access_token
)


def register_user(
    db: Session,
    user_data: UserRegister
):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:

        return None

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=get_password_hash(
            user_data.password
        ),
        role=user_data.role,
        is_active=True
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


def login_user(
    db: Session,
    login_data: UserLogin
):

    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:

        return None

    if not verify_password(
        login_data.password,
        user.hashed_password
    ):

        return None

    token = create_access_token(
        {
            "sub": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }