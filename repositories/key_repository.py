from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from models import Key
from schemas import KeyCreate, KeyUpdate


class KeyRepository:
    def __init__(self, database: Session):
        self.database = database

    def get_all(self) -> list[Key]:
        statement = (
            select(Key)
            .options(selectinload(Key.rooms))
            .order_by(Key.key_number)
        )
        return list(self.database.scalars(statement).all())

    def get_by_id(self, key_id: int) -> Key | None:
        statement = (
            select(Key)
            .options(selectinload(Key.rooms))
            .where(Key.id == key_id)
        )
        return self.database.scalar(statement)

    def create(self, key_data: KeyCreate) -> Key:
        key = Key(**key_data.model_dump())
        self.database.add(key)
        self.database.commit()
        self.database.refresh(key)
        return key

    def update(self, key: Key, key_data: KeyUpdate) -> Key:
        for field, value in key_data.model_dump(exclude_unset=True).items():
            setattr(key, field, value)

        self.database.commit()
        self.database.refresh(key)
        return key
