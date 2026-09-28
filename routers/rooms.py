from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from extensions import get_db
from repositories.room_repository import RoomRepository
from schemas import RoomCreate, RoomRead, RoomUpdate


router = APIRouter(prefix="/rooms", tags=["Rooms"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[RoomRead])
def list_rooms(database: DatabaseSession):
    return RoomRepository(database).get_all()


@router.get("/{room_id}", response_model=RoomRead)
def get_room(room_id: int, database: DatabaseSession):
    room = RoomRepository(database).get_by_id(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Raum nicht gefunden")
    return room


@router.post("", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
def create_room(room_data: RoomCreate, database: DatabaseSession):
    try:
        return RoomRepository(database).create(room_data)
    except IntegrityError as error:
        database.rollback()
        raise HTTPException(
            status_code=409,
            detail="Raumnummer ist bereits vergeben",
        ) from error


@router.patch("/{room_id}", response_model=RoomRead)
def update_room(
    room_id: int,
    room_data: RoomUpdate,
    database: DatabaseSession,
):
    repository = RoomRepository(database)
    room = repository.get_by_id(room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Raum nicht gefunden")

    try:
        return repository.update(room, room_data)
    except IntegrityError as error:
        database.rollback()
        raise HTTPException(
            status_code=409,
            detail="Raumnummer ist bereits vergeben",
        ) from error
