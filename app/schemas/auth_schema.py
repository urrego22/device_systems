from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    ConfigDict
)

import re


class UserRegister(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str

    role: str = Field(
        default="user"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 8:
            raise ValueError(
                "Password must contain at least 8 characters"
            )

        if " " in value:
            raise ValueError(
                "Password cannot contain spaces"
            )

        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain one uppercase letter"
            )

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain one lowercase letter"
            )

        if not re.search(r"\d", value):
            raise ValueError(
                "Password must contain one number"
            )

        return value


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class Token(BaseModel):

    access_token: str

    token_type: str


class TokenData(BaseModel):

    email: str | None = None


class UserResponse(BaseModel):

    id: int

    name: str

    email: str

    role: str

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )