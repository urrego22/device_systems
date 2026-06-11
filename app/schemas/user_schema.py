from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"


class UserCreate(BaseModel):
    """Schema para CREAR un usuario — usado en POST"""
    name: str = Field(..., min_length=3, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido y único")
    role: RoleEnum = Field(..., description="Rol: admin, support o user")
    is_active: bool = Field(default=True, description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sara García",
                "email": "sara@mail.com",
                "role": "admin",
                "is_active": True
            }
        }
    }


class UserUpdate(BaseModel):
    """Schema para actualización COMPLETA — usado en PUT"""
    name: str = Field(..., min_length=3, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico válido y único")
    role: RoleEnum = Field(..., description="Rol: admin, support o user")
    is_active: bool = Field(..., description="Estado del usuario")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sara García Actualizada",
                "email": "sara.nueva@mail.com",
                "role": "support",
                "is_active": True
            }
        }
    }


class UserPatch(BaseModel):
    """Schema para actualización PARCIAL — usado en PATCH"""
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "role": "support"
            }
        }
    }


class UserResponse(BaseModel):
    """Schema de respuesta — lo que la API devuelve al cliente"""
    id: int
    name: str
    email: str
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}