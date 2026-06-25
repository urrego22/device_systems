from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.connection import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    serial_number = Column(
        String,
        unique=True,
        nullable=False
    )

    device_type = Column(String, nullable=False)

    brand = Column(String, nullable=True)

    is_available = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    owner = relationship(
        "User",
        back_populates="devices"
    )

    loans = relationship(
        "Loan",
        back_populates="device"
    )