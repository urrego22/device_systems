from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=2)
    serial_number: str = Field(..., min_length=3)
    device_type: str = Field(..., description="laptop, tablet, proyector, camara, router, monitor")
    brand: Optional[str] = None
    is_available: bool = True
    user_id: Optional[int] = None


class DeviceUpdate(BaseModel):
    name: str = Field(..., min_length=2)
    serial_number: str = Field(..., min_length=3)
    device_type: str
    brand: Optional[str] = None
    is_available: bool = True
    user_id: Optional[int] = None


class DevicePatch(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None
    user_id: Optional[int] = None


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str] = None
    is_available: bool
    created_at: Optional[datetime] = None
    user_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }