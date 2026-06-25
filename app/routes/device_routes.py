from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin
)
from app.models.user_model import User

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DevicePatch,
    DeviceResponse
)
from app.schemas.loan_schema import LoanResponse

from app.services import device_service, loan_service


router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get(
    "/",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos con filtros opcionales"
)
def get_devices(
    device_type: Optional[str] = None,
    brand: Optional[str] = None,
    is_available: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return device_service.get_all_devices(
        db,
        device_type=device_type,
        brand=brand,
        is_available=is_available,
        search=search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID"
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return device_service.get_device_by_id(db, device_id)


@router.get(
    "/{device_id}/loans",
    response_model=list[LoanResponse],
    summary="Historial de préstamos de un dispositivo",
    description="Usa join entre Loan y User para obtener historial completo del dispositivo."
)
def get_device_loans(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return loan_service.get_loans_by_device(db, device_id)


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo (admin o support)"
)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    return device_service.create_device(db, device_data)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo (admin o support)"
)
def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    return device_service.update_device(db, device_id, device_data)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcialmente (admin o support)"
)
def patch_device(
    device_id: int,
    device_data: DevicePatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role not in ["admin", "support"]:
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    return device_service.patch_device(db, device_id, device_data)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo (solo admin)"
)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    device_service.delete_device(db, device_id)