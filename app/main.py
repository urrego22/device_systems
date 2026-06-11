from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes.user_routes import router

# Crea todas las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description="""
## device_systems API REST v3.0.0

API REST para la gestión de usuarios con **persistencia real en base de datos SQLite**.

Desarrollada por **Sara García** — SENA.

### ¿Qué hay de nuevo en v3.0.0?
- Persistencia real con **SQLAlchemy + SQLite**
-  Modelo `User` en base de datos con constraints
-  Campo `created_at` con fecha automática
-  Sesiones de base de datos con `Depends(get_db)`
-  CRUD completo sobre base de datos real

### Roles permitidos: `admin` | `support` | `user`
    """,
    version="3.0.0",
    contact={"name": "Sara García", "email": "sara.garcia@devicesystems.com"},
    openapi_tags=[{
        "name": "Users",
        "description": "CRUD completo de usuarios con persistencia en base de datos SQLite."
    }]
)

app.include_router(router)


@app.get("/", tags=["Root"], summary="Bienvenida")
def root():
    return {
        "message": "Bienvenida a device_systems API v3.0.0",
        "author": "Sara García",
        "database": "SQLite — SQLAlchemy ORM",
        "docs": "/docs",
        "redoc": "/redoc"
    }