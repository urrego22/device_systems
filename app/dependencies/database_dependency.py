from app.database.connection import SessionLocal


def get_db():
    """
    Dependencia reutilizable que entrega una sesión de base de datos.
    Se usa con Depends() en los endpoints.
    Cierra la sesión automáticamente al terminar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()