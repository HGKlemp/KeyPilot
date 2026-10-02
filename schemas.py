from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


EmployeeRole = Literal["employee", "operator"]
KeyStatus = Literal["available", "issued", "lost", "defective", "retired"]


class EmployeeCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)
    role: EmployeeRole = "employee"
    auth0_id: str | None = Field(default=None, max_length=255)
    active: bool = True


class EmployeeUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=3, max_length=255)
    role: EmployeeRole | None = None
    auth0_id: str | None = Field(default=None, max_length=255)
    active: bool | None = None


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: str
    role: EmployeeRole
    auth0_id: str | None
    active: bool
    created_at: datetime


class RoomCreate(BaseModel):
    room_number: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    building: str | None = Field(default=None, max_length=100)
    floor: str | None = Field(default=None, max_length=50)
    active: bool = True


class RoomUpdate(BaseModel):
    room_number: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    building: str | None = Field(default=None, max_length=100)
    floor: str | None = Field(default=None, max_length=50)
    active: bool | None = None


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


class KeyCreate(BaseModel):
    key_number: str = Field(min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    storage_location: str | None = Field(default=None, max_length=100)
    status: KeyStatus = "available"


class KeyUpdate(BaseModel):
    key_number: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    storage_location: str | None = Field(default=None, max_length=100)
    status: KeyStatus | None = None


class LoanCreate(BaseModel):
    key_id: int = Field(gt=0)
    employee_id: int = Field(gt=0)
    issued_by_operator_id: int = Field(gt=0)
    notes: str | None = None


class LoanReturn(BaseModel):
    returned_by_operator_id: int = Field(gt=0)


class LoanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key_id: int
    employee_id: int
    issued_by_operator_id: int
    issued_at: datetime
    returned_by_operator_id: int | None
    returned_at: datetime | None
    notes: str | None
