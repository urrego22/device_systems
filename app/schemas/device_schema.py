from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=2)
    serial_number: str = Field(..., min_length=3)
    user_id: int


class DeviceUpdate(BaseModel):
    name: str = Field(..., min_length=2)
    serial_number: str = Field(..., min_length=3)
    user_id: int


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    user_id: int | None = None

    model_config = {
        "from_attributes": True
    }