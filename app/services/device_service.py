from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.models.device_model import Device
from app.models.user_model import User
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch


def get_all_devices(
    db: Session,
    device_type: Optional[str] = None,
    brand: Optional[str] = None,
    is_available: Optional[bool] = None,
    search: Optional[str] = None
):
    query = db.query(Device)

    if device_type:
        query = query.filter(
            Device.device_type.ilike(f"%{device_type}%")
        )

    if brand:
        query = query.filter(
            Device.brand.ilike(f"%{brand}%")
        )

    if is_available is not None:
        query = query.filter(
            Device.is_available == is_available
        )

    if search:
        query = query.filter(
            Device.name.ilike(f"%{search}%")
        )

    return query.all()


def get_device_by_id(db: Session, device_id: int):

    device = db.query(Device).filter(
        Device.id == device_id
    ).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return device


def create_device(db: Session, device_data: DeviceCreate):

    existing = db.query(Device).filter(
        Device.serial_number == device_data.serial_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un dispositivo con ese número de serie"
        )

    if device_data.user_id:
        user = db.query(User).filter(
            User.id == device_data.user_id
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

    device = Device(
        name=device_data.name,
        serial_number=device_data.serial_number,
        device_type=device_data.device_type,
        brand=device_data.brand,
        is_available=device_data.is_available,
        user_id=device_data.user_id
    )

    db.add(device)
    db.commit()
    db.refresh(device)

    return device


def update_device(
    db: Session,
    device_id: int,
    device_data: DeviceUpdate
):
    device = get_device_by_id(db, device_id)

    device.name = device_data.name
    device.serial_number = device_data.serial_number
    device.device_type = device_data.device_type
    device.brand = device_data.brand
    device.is_available = device_data.is_available
    device.user_id = device_data.user_id

    db.commit()
    db.refresh(device)

    return device


def patch_device(
    db: Session,
    device_id: int,
    device_data: DevicePatch
):
    device = get_device_by_id(db, device_id)

    update_data = device_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)

    return device


def delete_device(db: Session, device_id: int):

    device = get_device_by_id(db, device_id)
    db.delete(device)
    db.commit()