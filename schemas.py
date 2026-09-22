from pydantic import BaseModel, ConfigDict


class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_number: str
    name: str
    building: str | None
    floor: str | None
    active: bool


class KeyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key_number: str
    description: str | None
    storage_location: str | None
    status: str
    rooms: list[RoomRead]
