from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.loan_schema import (
    LoanCreate,
    LoanUpdate,
    LoanResponse
)

from app.services import loan_service


router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.get("/", response_model=list[LoanResponse])
def get_loans(db: Session = Depends(get_db)):
    return loan_service.get_all_loans(db)


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    return loan_service.get_loan_by_id(db, loan_id)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED
)
def create_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db)
):
    return loan_service.create_loan(db, loan_data)


@router.put("/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: int,
    loan_data: LoanUpdate,
    db: Session = Depends(get_db)
):
    return loan_service.update_loan(
        db,
        loan_id,
        loan_data
    )


@router.delete("/{loan_id}")
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db)
):
    loan_service.delete_loan(db, loan_id)

    return {
        "message": "Préstamo eliminado"
    }