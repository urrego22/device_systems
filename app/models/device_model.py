from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

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

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="devices"
    )

    loans = relationship(
    "Loan",
    back_populates="device"
)