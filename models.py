from extensions import db

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
    employee_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True, nullable=False)

class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True, nullable=False)

class Key(db.Model):
    __tablename__ = "keys"

    id = db.Column(db.Integer, primary_key=True)
    key_number = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(100))
    status = db.Column(db.String(20), default="available", nullable=False)
    rooms = db.relationship(
        "Room",
        secondary=key_rooms,
        backref="keys",
    )