from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from extensions import get_db
from models import Key
from schemas import KeyRead


app = FastAPI(
    title="KeyPilot API",
    version="0.1.0",
    description="Backend zur Verwaltung von Schlüsseln, Räumen und Ausleihen.",
)

DatabaseSession = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root():
    return {"name": "KeyPilot API", "status": "ok"}


@app.get("/keys", response_model=list[KeyRead])
def list_keys(database: DatabaseSession):
    statement = (
        select(Key)
        .options(selectinload(Key.rooms))
        .order_by(Key.key_number)
    )
    return database.scalars(statement).all()


@app.get("/keys/{key_id}", response_model=KeyRead)
def get_key(key_id: int, database: DatabaseSession):
    statement = (
        select(Key)
        .options(selectinload(Key.rooms))
        .where(Key.id == key_id)
    )
    key = database.scalar(statement)

    if key is None:
        raise HTTPException(status_code=404, detail="Schlüssel nicht gefunden")

    return key
