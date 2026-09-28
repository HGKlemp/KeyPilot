from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Room
from schemas import RoomCreate, RoomUpdate


class RoomRepository:
    def __init__(self, database: Session):
        self.database = database

    def get_all(self) -> list[Room]:
        statement = select(Room).order_by(Room.room_number)
        return list(self.database.scalars(statement).all())

    def get_by_id(self, room_id: int) -> Room | None:
        return self.database.get(Room, room_id)

    def create(self, room_data: RoomCreate) -> Room:
        room = Room(**room_data.model_dump())
        self.database.add(room)
        self.database.commit()
        self.database.refresh(room)
        return room

    def update(self, room: Room, room_data: RoomUpdate) -> Room:
        for field, value in room_data.model_dump(exclude_unset=True).items():
            setattr(room, field, value)

        self.database.commit()
        self.database.refresh(room)
        return room
