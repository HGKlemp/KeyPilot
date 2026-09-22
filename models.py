from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    text,
)
from sqlalchemy.orm import relationship

from extensions import Base


EMPLOYEE_ROLES = ("employee", "operator")
KEY_STATUSES = ("available", "issued", "lost", "defective", "retired")


key_rooms = Table(
    "key_rooms",
    Base.metadata,
    Column("key_id", Integer, ForeignKey("keys.id"), primary_key=True),
    Column("room_id", Integer, ForeignKey("rooms.id"), primary_key=True),
)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(
        Enum(*EMPLOYEE_ROLES, name="employee_role"),
        default="employee",
        nullable=False,
    )
    auth0_id = Column(String(255), unique=True)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_number = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    building = Column(String(100))
    floor = Column(String(50))
    active = Column(Boolean, default=True, nullable=False)

    keys = relationship("Key", secondary=key_rooms, back_populates="rooms")


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True)
    key_number = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    storage_location = Column(String(100))
    status = Column(
        Enum(*KEY_STATUSES, name="key_status"),
        default="available",
        nullable=False,
    )

    rooms = relationship("Room", secondary=key_rooms, back_populates="keys")


class KeyLoan(Base):
    __tablename__ = "key_loans"

    id = Column(Integer, primary_key=True)
    key_id = Column(Integer, ForeignKey("keys.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    issued_by_operator_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
    )
    issued_at = Column(
        DateTime(timezone=True),
        server_default=text("now()"),
        nullable=False,
    )
    returned_by_operator_id = Column(Integer, ForeignKey("employees.id"))
    returned_at = Column(DateTime(timezone=True))
    notes = Column(Text)

    employee = relationship("Employee", foreign_keys=[employee_id])
    key = relationship("Key")
    issued_by_operator = relationship(
        "Employee",
        foreign_keys=[issued_by_operator_id],
    )
    returned_by_operator = relationship(
        "Employee",
        foreign_keys=[returned_by_operator_id],
    )

    __table_args__ = (
        Index(
            "uq_open_key_loan",
            "key_id",
            unique=True,
            postgresql_where=text("returned_at IS NULL"),
        ),
    )
