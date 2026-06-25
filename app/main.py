from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded

from slowapi.middleware import SlowAPIMiddleware

from slowapi import _rate_limit_exceeded_handler

from app.rate_limiter import limiter

from app.database.connection import (
    engine,
    Base
)

from app.routes.user_routes import (
    router as user_router
)

from app.routes.device_routes import (
    router as device_router
)

from app.routes.loan_routes import (
    router as loan_router
)

from app.auth.auth_routes import (
    router as auth_router
)

from app.middlewares.request_middleware import (
    request_middleware
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(

    title="device_systems API",

    description="""
# Proyecto Final V1 - FastAPI Seguridad

API REST segura para la gestión de:

- Usuarios
- Dispositivos
- Préstamos

Tecnologías implementadas:

- SQLAlchemy
- Alembic
- OAuth2
- JWT
- Passlib
- Middleware personalizado
- CORS
- Rate Limiting
- Validaciones avanzadas con Pydantic v2

Proyecto académico SENA.
""",

    version="3.0.0",

    contact={

        "name": "Sara García Urrego",

        "email": "estudiante@sena.edu.co"
    }
)


# RATE LIMITING

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
)


# MIDDLEWARE

app.middleware("http")(
    request_middleware
)


# CORS

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",

        "http://localhost:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# RUTAS

app.include_router(
    user_router
)

app.include_router(
    device_router
)

app.include_router(
    loan_router
)

app.include_router(
    auth_router
)


@app.get("/")
def root():

    return {

        "message": "Bienvenido al Proyecto Final V2",

        "project": "device_systems",

        "version": "3.0.0",

        "database": "SQLite"
    }