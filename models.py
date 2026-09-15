from extensions import db


EMPLOYEE_ROLES = ("employee", "operator")
KEY_STATUSES = ("available", "issued", "lost", "defective", "retired")


key_rooms = db.Table(
    "key_rooms",
    db.Column(
        "key_id",
        db.Integer,
        db.ForeignKey("keys.id"),
        primary_key=True,
    ),
    db.Column(
        "room_id",
        db.Integer,
        db.ForeignKey("rooms.id"),
        primary_key=True,
    ),
)


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(
        db.Enum(*EMPLOYEE_ROLES, name="employee_role"),
        default="employee",
        nullable=False,
    )
    auth0_id = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        nullable=False,
    )


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(100))
    floor = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True, nullable=False)

    keys = db.relationship(
        "Key",
        secondary=key_rooms,
        back_populates="rooms",
    )


class Key(db.Model):
    __tablename__ = "keys"

    id = db.Column(db.Integer, primary_key=True)
    key_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    storage_location = db.Column(db.String(100))
    status = db.Column(
        db.Enum(*KEY_STATUSES, name="key_status"),
        default="available",
        nullable=False,
    )

    rooms = db.relationship(
        "Room",
        secondary=key_rooms,
        back_populates="keys",
    )


class KeyLoan(db.Model):
    __tablename__ = "key_loans"

    id = db.Column(db.Integer, primary_key=True)
    key_id = db.Column(
        db.Integer,
        db.ForeignKey("keys.id"),
        nullable=False,
    )
    employee_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False,
    )
    issued_by_operator_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
        nullable=False,
    )
    issued_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        nullable=False,
    )
    returned_by_operator_id = db.Column(
        db.Integer,
        db.ForeignKey("employees.id"),
    )
    returned_at = db.Column(db.DateTime(timezone=True))
    notes = db.Column(db.Text)

    employee = db.relationship("Employee", foreign_keys=[employee_id])
    key = db.relationship("Key")
    issued_by_operator = db.relationship(
        "Employee",
        foreign_keys=[issued_by_operator_id],
    )
    returned_by_operator = db.relationship(
        "Employee",
        foreign_keys=[returned_by_operator_id],
    )

    __table_args__ = (
        db.Index(
            "uq_open_key_loan",
            "key_id",
            unique=True,
            postgresql_where=db.text("returned_at IS NULL"),
        ),
    )
