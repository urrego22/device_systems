from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    loan_date = Column(Date, nullable=False)

    return_date = Column(Date, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    device_id = Column(
        Integer,
        ForeignKey("devices.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="loans"
    )

    device = relationship(
        "Device",
        back_populates="loans"
    )