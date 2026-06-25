from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi import Request

from app.rate_limiter import limiter

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse
)

from app.auth.auth_service import (
    register_user,
    login_user
)

from app.dependencies.auth_dependency import (
    get_current_active_user
)

from app.models.user_model import User


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)

@limiter.limit("3/minute")
def register(
    request: Request,

    user: UserRegister,

    db: Session = Depends(get_db)
):

    new_user = register_user(
        db,
        user
    )

    if not new_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return new_user


@router.post(
    "/login",
    response_model=Token
)

@limiter.limit("5/minute")

def login(
    request: Request,

    form_data: OAuth2PasswordRequestForm = Depends(),

    db: Session = Depends(get_db)
):

    login_data = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    token = login_user(
        db,
        login_data
    )

    if not token:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return token


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(
        get_current_active_user
    )
):

    return current_user