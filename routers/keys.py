from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from extensions import get_db
from repositories.key_repository import KeyRepository
from schemas import KeyRead


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
