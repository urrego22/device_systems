from fastapi import FastAPI
from app.database.connection import engine, Base

from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Systems API",
    description="""
# Proyecto Final V1 - FastAPI Avanzado

Sistema para la gestión de:

- Users
- Devices
- Loans

Características implementadas:

- FastAPI
- SQLAlchemy ORM
- SQLite
- Alembic
- Relaciones entre modelos
- Foreign Keys
- Joins
- Filtros avanzados
- Swagger / OpenAPI

Desarrollado para la evidencia EV10.
""",
    version="1.0.0",
    contact={
        "name": "Luis Diego",
        "email": "estudiante@sena.edu.co"
    }
)

# Rutas
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get(
    "/",
    tags=["Root"],
    summary="Bienvenida"
)
def root():
    return {
        "message": "Bienvenido al Proyecto Final V1",
        "project": "Device Systems",
        "version": "1.0.0",
        "database": "SQLite",
        "docs": "/docs",
        "redoc": "/redoc"
    }