from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.user_model import User
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


def get_all_devices(db: Session):
    return db.query(Device).all()


def get_device_by_id(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Dispositivo no encontrado"
        )

    return device


def create_device(db: Session, device_data: DeviceCreate):

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
    device.user_id = device_data.user_id

    db.commit()
    db.refresh(device)

    return device


def delete_device(db: Session, device_id: int):

    device = get_device_by_id(db, device_id)

    db.delete(device)
    db.commit()