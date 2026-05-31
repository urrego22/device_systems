# Base de datos simulada en memoria
# Movida desde user_routes.py para separar responsabilidades

fake_db: list = [
    {"id": 1, "name": "Ana Torres", "email": "ana@mail.com",
     "role": "admin", "is_active": True},
    {"id": 2, "name": "Carlos López", "email": "carlos@mail.com",
     "role": "support", "is_active": True},
    {"id": 3, "name": "María Pérez", "email": "maria@mail.com",
     "role": "user", "is_active": False},
]