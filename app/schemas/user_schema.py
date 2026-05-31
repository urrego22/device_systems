from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: RoleEnum = Field(..., description="Rol: admin, support o user")
    is_active: bool = Field(default=True)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laura Gómez",
                "email": "laura@mail.com",
                "role": "support",
                "is_active": True
            }
        }
    }


class UserUpdate(BaseModel):
    """Esquema para actualización COMPLETA (PUT) — todos los campos requeridos"""
    name: str = Field(..., min_length=3, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: RoleEnum = Field(..., description="Rol: admin, support o user")
    is_active: bool = Field(..., description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ana Torres Actualizada",
                "email": "ana.nueva@mail.com",
                "role": "admin",
                "is_active": True
            }
        }
    }


class UserPartialUpdate(BaseModel):
    """Esquema para actualización PARCIAL (PATCH) — todos los campos opcionales"""
    name: Optional[str] = Field(None, min_length=3, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico válido")
    role: Optional[RoleEnum] = Field(None, description="Rol: admin, support o user")
    is_active: Optional[bool] = Field(None, description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "support"
            }
        }
    }


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum
    is_active: bool

    model_config = {"from_attributes": True}