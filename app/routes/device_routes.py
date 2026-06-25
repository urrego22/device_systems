from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin
)

from app.models.user_model import User

from app.schemas.device_schema import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse
)

from app.services import device_service


router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)


@router.get(
    "/",
    response_model=list[DeviceResponse]
)
def get_devices(
    db: Session = Depends(get_db)
):

    return device_service.get_all_devices(db)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db)
):

    return device_service.get_device_by_id(
        db,
        device_id
    )


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_device(
    device_data: DeviceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    if current_user.role not in [
        "admin",
        "support"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    return device_service.create_device(
        db,
        device_data
    )


@router.put(
    "/{device_id}",
    response_model=DeviceResponse
)
def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_active_user
    )
):

    if current_user.role not in [
        "admin",
        "support"
    ]:

        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    return device_service.update_device(
        db,
        device_id,
        device_data
    )


@router.delete(
    "/{device_id}"
)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_admin
    )
):

    device_service.delete_device(
        db,
        device_id
    )

    return {
        "message": "Dispositivo eliminado"
    }