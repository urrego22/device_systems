from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import date
from typing import Optional

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device

from app.schemas.loan_schema import (
    LoanCreate,
    LoanUpdate
)


def get_all_loans(
    db: Session,
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None
):
    """
    Consulta préstamos con joins y filtros avanzados.
    Usa join() con User y Device para filtrar por sus campos.
    """
    query = db.query(Loan).join(
        User, Loan.user_id == User.id
    ).join(
        Device, Loan.device_id == Device.id
    )

    if status:
        query = query.filter(Loan.status == status)

    if user_email:
        query = query.filter(
            User.email.ilike(f"%{user_email}%")
        )

    if device_type:
        query = query.filter(
            Device.device_type.ilike(f"%{device_type}%")
        )

    return query.all()


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


def get_loan_details(db: Session):
    """
    Retorna préstamos con información completa de usuario y dispositivo.
    Usa join() explícito entre Loan, User y Device.
    """
    loans = db.query(Loan).join(
        User, Loan.user_id == User.id
    ).join(
        Device, Loan.device_id == Device.id
    ).all()

    result = []
    for loan in loans:
        result.append({
            "loan_id": loan.id,
            "status": loan.status,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date,
            "user": {
                "id": loan.user.id,
                "name": loan.user.name,
                "email": loan.user.email
            },
            "device": {
                "id": loan.device.id,
                "name": loan.device.name,
                "serial_number": loan.device.serial_number,
                "device_type": loan.device.device_type
            }
        })

    return result


def get_loans_by_user(db: Session, user_id: int):
    """
    Consulta préstamos de un usuario específico usando join.
    """
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    loans = db.query(Loan).join(
        Device, Loan.device_id == Device.id
    ).filter(
        Loan.user_id == user_id
    ).all()

    return loans


def get_loans_by_device(db: Session, device_id: int):
    """
    Consulta historial de préstamos de un dispositivo.
    """
    device = db.query(Device).filter(
        Device.id == device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    loans = db.query(Loan).join(
        User, Loan.user_id == User.id
    ).filter(
        Loan.device_id == device_id
    ).all()

    return loans


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

    if not device.is_available:
        raise HTTPException(
            status_code=409,
            detail="El dispositivo no está disponible para préstamo"
        )

    loan = Loan(
        loan_date=loan_data.loan_date,
        return_date=loan_data.return_date,
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        status="active"
    )

    device.is_available = False

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


def return_loan(db: Session, loan_id: int):

    loan = get_loan_by_id(db, loan_id)

    if loan.status == "returned":
        raise HTTPException(
            status_code=409,
            detail="Este préstamo ya fue devuelto"
        )

    loan.status = "returned"
    loan.return_date = date.today()

    device = db.query(Device).filter(
        Device.id == loan.device_id
    ).first()

    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)

    return loan


def delete_loan(db: Session, loan_id: int):

    loan = get_loan_by_id(db, loan_id)
    db.delete(loan)
    db.commit()