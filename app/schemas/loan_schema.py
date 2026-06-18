from datetime import date
from pydantic import BaseModel


class LoanCreate(BaseModel):
    loan_date: date
    return_date: date | None = None
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    loan_date: date
    return_date: date | None = None
    user_id: int
    device_id: int


class LoanResponse(BaseModel):
    id: int
    loan_date: date
    return_date: date | None = None
    user_id: int
    device_id: int

    model_config = {
        "from_attributes": True
    }