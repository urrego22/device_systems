from fastapi import FastAPI
from app.routes.user_routes import router

app = FastAPI(
    title="device_systems API",
    description="""
##  device_systems API REST v2.0.0

API REST para la gestión de usuarios del sistema **device_systems**.

Desarrollada por **Sara García** — SENA.

### Operaciones disponibles
-  Listar usuarios con filtros por rol y estado
-  Consultar usuario por ID
-  Crear usuario
-  Actualizar completamente (PUT)
-  Actualizar parcialmente (PATCH)
-  Eliminar usuario

### Roles permitidos: `admin` | `support` | `user`
    """,
    version="2.0.0",
    contact={"name": "Sara García", "email": "sara.garcia@devicesystems.com"},
    openapi_tags=[{
        "name": "Users",
        "description": "CRUD completo de gestión de usuarios con validaciones y manejo de errores."
    }]
)

app.include_router(router)


@app.get("/", tags=["Root"], summary="Bienvenida a la API")
def root():
    return {
        "message": "Bienvenida a device_systems API v2.0.0",
        "author": "Sara García",
        "docs": "/docs",
        "redoc": "/redoc"
    }