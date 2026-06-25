from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin
)
from app.models.user_model import User

from app.schemas.loan_schema import (
    LoanCreate,
    LoanResponse,
    LoanDetailResponse
)

from app.services import loan_service


router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.get(
    "/details",
    summary="Listar préstamos con detalle de usuario y dispositivo",
    description="Usa JOIN entre Loan, User y Device para retornar información completa."
)
def get_loan_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.get_loan_details(db)


@router.get(
    "/",
    response_model=list[LoanResponse],
    summary="Listar préstamos con filtros opcionales",
    description="Filtra por status, email de usuario o tipo de dispositivo usando joins."
)
def get_loans(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.get_all_loans(
        db,
        status=status,
        user_email=user_email,
        device_type=device_type
    )


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Obtener préstamo por ID"
)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.get_loan_by_id(db, loan_id)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Valida que el usuario y dispositivo existan y que el dispositivo esté disponible."
)
def create_loan(
    loan_data: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.create_loan(db, loan_data)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Marca el préstamo como 'returned' y libera el dispositivo (is_available=True)."
)
def return_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.return_loan(db, loan_id)


@router.delete(
    "/{loan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar préstamo"
)
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    loan_service.delete_loan(db, loan_id)