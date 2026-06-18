from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device

from app.schemas.loan_schema import (
    LoanCreate,
    LoanUpdate
)


def get_all_loans(db: Session):
    return db.query(Loan).all()


def get_loan_by_id(db: Session, loan_id: int):

    loan = db.query(Loan).filter(
        Loan.id == loan_id
    ).first()

    if not loan:
        raise HTTPException(
            status_code=404,
            detail="Préstamo no encontrado"
        )

    return loan


def create_loan(db: Session, loan_data: LoanCreate):

    user = db.query(User).filter(
        User.id == loan_data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    device = db.query(Device).filter(
        Device.id == loan_data.device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    loan = Loan(
        loan_date=loan_data.loan_date,
        return_date=loan_data.return_date,
        user_id=loan_data.user_id,
        device_id=loan_data.device_id
    )

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


def update_loan(
    db: Session,
    loan_id: int,
    loan_data: LoanUpdate
):

    loan = get_loan_by_id(db, loan_id)

    loan.loan_date = loan_data.loan_date
    loan.return_date = loan_data.return_date
    loan.user_id = loan_data.user_id
    loan.device_id = loan_data.device_id

    db.commit()
    db.refresh(loan)

    return loan


def delete_loan(db: Session, loan_id: int):

    loan = get_loan_by_id(db, loan_id)

    db.delete(loan)
    db.commit()