from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserInLoan(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


class DeviceInLoan(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}


class LoanCreate(BaseModel):
    loan_date: date
    return_date: Optional[date] = None
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    loan_date: date
    return_date: Optional[date] = None
    user_id: int
    device_id: int
    status: str = Field(default="active")


class LoanResponse(BaseModel):
    id: int
    loan_date: date
    return_date: Optional[date] = None
    status: str
    user_id: int
    device_id: int

    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: date
    return_date: Optional[date] = None
    user: UserInLoan
    device: DeviceInLoan

    model_config = {"from_attributes": True}