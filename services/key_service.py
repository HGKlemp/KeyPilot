from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Key
from repositories.key_repository import KeyRepository
from schemas import KeyCreate, KeyUpdate


class KeyNotFoundError(Exception):
    pass


class KeyConflictError(Exception):
    pass


class KeyService:
    def __init__(self, database: Session):
        self.database = database
        self.repository = KeyRepository(database)

    def create_key(self, key_data: KeyCreate) -> Key:
        if key_data.status == "issued":
            raise KeyConflictError(
                "Der Status 'issued' wird nur durch eine Ausleihe gesetzt"
            )

        try:
            return self.repository.create(key_data)
        except IntegrityError as error:
            self.database.rollback()
            raise KeyConflictError("Schlüsselnummer ist bereits vergeben") from error

    def update_key(self, key_id: int, key_data: KeyUpdate) -> Key:
        key = self.repository.get_by_id(key_id)

        if key is None:
            raise KeyNotFoundError("Schlüssel nicht gefunden")

        if key_data.status == "issued":
            raise KeyConflictError(
                "Der Status 'issued' wird nur durch eine Ausleihe gesetzt"
            )

        if key.status == "issued" and key_data.status is not None:
            raise KeyConflictError(
                "Der Status eines ausgeliehenen Schlüssels kann nicht geändert werden"
            )

        try:
            return self.repository.update(key, key_data)
        except IntegrityError as error:
            self.database.rollback()
            raise KeyConflictError("Schlüsselnummer ist bereits vergeben") from error
