from pydantic import BaseModel, Field, field_validator, ConfigDict


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(..., description="Email válido")
    password: str = Field(..., min_length=8)
    role: str = Field(default="user")

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if " " in v:
            raise ValueError("La contraseña no puede tener espacios")
        if not any(c.isupper() for c in v):
            raise ValueError("Debe tener al menos una mayúscula")
        if not any(c.islower() for c in v):
            raise ValueError("Debe tener al menos una minúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("Debe tener al menos un número")
        return v


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)


class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None