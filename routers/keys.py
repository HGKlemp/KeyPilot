from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from extensions import get_db
from repositories.key_repository import KeyRepository
from schemas import KeyCreate, KeyRead, KeyUpdate
from services.key_service import KeyConflictError, KeyNotFoundError, KeyService


router = APIRouter(prefix="/keys", tags=["Keys"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[KeyRead])
def list_keys(database: DatabaseSession):
    repository = KeyRepository(database)
    return repository.get_all()


@router.get("/{key_id}", response_model=KeyRead)
def get_key(key_id: int, database: DatabaseSession):
    repository = KeyRepository(database)
    key = repository.get_by_id(key_id)

    if key is None:
        raise HTTPException(status_code=404, detail="Schlüssel nicht gefunden")

    return key


@router.post("", response_model=KeyRead, status_code=status.HTTP_201_CREATED)
def create_key(key_data: KeyCreate, database: DatabaseSession):
    try:
        return KeyService(database).create_key(key_data)
    except KeyConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.patch("/{key_id}", response_model=KeyRead)
def update_key(
    key_id: int,
    key_data: KeyUpdate,
    database: DatabaseSession,
):
    try:
        return KeyService(database).update_key(key_id, key_data)
    except KeyNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except KeyConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
